package graph

import scala.collection.mutable
import scala.collection.mutable.ArrayBuffer
import scala.math.Ordered._

case class Node[A:Ordering](label: A) extends Ordered[Node[A]] {
  override def compare(that: Node[A]): Int = this.label compare that.label
}

// making Node extend Ordered is necessary for comparisons
// adding the Ordering object is necessary for sorting.
// doesn't make sense; don't we get converters to change one into the other?

object Node {
  implicit def toNode[A:Ordering](label: A) = Node[A](label)
  implicit def ord[A:Ordering]: Ordering[Node[A]] = Ordering.by(_.label)
  def apply[A:Ordering](label: A): Node[A] = new Node[A](label)
}

// graph is a map of nodes to sets of nodes
class Graph[A:Ordering] extends mutable.HashMap[Node[A], scala.collection.mutable.Set[Node[A]]] {
  def addNode(n: Node[A]): Unit = {
    if (this.contains(n)) {
      throw new IllegalStateException("node already in graph")
    }
    else {
      this += (n -> mutable.Set[Node[A]]())
    }
  }

  def addNodes(n: Node[A]*): Unit = {
    for (elem <- n) {
      this.addNode(elem)
    }
  }

  def addEdge(a: Node[A], b: Node[A]): Unit = {
    if (!this.contains(a)) throw new IllegalStateException(s"node $a not in graph")
    if (!this.contains(b)) throw new IllegalStateException(s"node $b not in graph")

    this (a).add(b)
  }

  def dfs(startHere: Node[A]): Array[String] = {
    // non-recursive implementation
    require(this.contains(startHere))

    val visited = mutable.HashSet[Node[A]]()
    val stack = mutable.Stack[Node[A]]()
    var result_buffer = ArrayBuffer[Node[A]]()

    stack.push(startHere)
    visited.add(startHere)
    result_buffer += startHere

    def next_unvisited_neighbor(n: Node[A]): Option[Node[A]] = {
      val adj_list = this(n).toList.sorted
      adj_list.filterNot(x => visited.contains(x)).headOption
    }

    while (stack.nonEmpty) {
      val top = stack.top
      val k = next_unvisited_neighbor(top)

      k match {
        case Some(x) => {
          stack.push(x)
          visited.add(x)
          result_buffer += x
        }
        case None => stack.pop()
      }
    }

    result_buffer.map(x => x.label.toString).toArray
  }

  def isBipartite(): Boolean = {
    // look for odd-length cycles.  if there are any, return False
    // non-recursive implementation

    val visited = mutable.HashSet[Node[A]]()

    def oddCycleHere(startHere:Node[A]): Boolean = {
      // do a DFS at startHere and return true iff an odd-length cycle exists from this node

      // per the scala Stack documentation, we will implement the stack as a list.
      // top is element 0.

      var stack = List[Node[A]]()

      stack = startHere :: stack
      visited.add(startHere)

      def next_unvisited_neighbor(n: Node[A]): Option[Node[A]] = {
        val adj_list = this(n).toList.sorted
        adj_list.filterNot(x => visited.contains(x)).headOption
      }

      def any_visited_neighbors(n: Node[A], antecedent: Option[Node[A]]): Boolean = {
        // look for any visited nodes in our adjacency list, but ignore the node that
        // precedes n in the current path.
        var adj_list = this(n).toList
        adj_list = antecedent match {
          case Some(x) => adj_list.filter(n => n != x)
          case _ => adj_list
        }
        val visited_neighbors = adj_list.filter(x => visited.contains(x))
        visited_neighbors.nonEmpty
      }

      var path_length = 0

      while (stack.nonEmpty) {
        val top = stack.head
        val antecedent: Option[Node[A]] = stack match {
          case x :: y :: rest => Some(y)
          case _ => None
        }

        // see if there are neighbors that we have visited
        if (path_length % 2 == 0 && any_visited_neighbors(top, antecedent)) {
          // we have an odd-length cycle - path_length is even but adding another edge gives a cycle
          return true
        }

        val k = next_unvisited_neighbor(top)

        k match {
          case Some(x) => {
            stack = x :: stack
            visited.add(x)
            path_length += 1
          }
          case None => {
            stack = stack.tail
            path_length -= 1
          }
        }
      }
      false
    }

    for (k <- keys) {
      if (!visited.contains(k)) {
        if (oddCycleHere(k)) {
          return false
        }
      }
    }
    true
  }

  def bfs(startHere: Node[A]): Array[String] = {
    require(this.contains(startHere))

    // use a Vector as a deque
    var deque = Vector[Node[A]]()
    var visited = mutable.HashSet[Node[A]]()

    deque = deque :+ startHere
    visited.add(startHere)
    var result_buffer = ArrayBuffer[Node[A]]()

    while (deque.nonEmpty) {
      val front: Node[A] = deque.take(1)(0)
      deque = deque.drop(1)
      result_buffer += front

      // enqueue all unvisited adj_list
      val adj_list = this(front).toList.sorted
      val unvisited = adj_list.filterNot(visited.contains(_))
      deque ++= unvisited
      visited ++= unvisited
    }
    result_buffer.map(x => x.label.toString).toArray
  }
}

object Graph {
  def apply[A:Ordering](): Graph[A] = new Graph[A]()
}

class UGraph[A:Ordering] extends Graph[A] {
  // undirected graph
  override def addEdge(a: Node[A], b: Node[A]): Unit = {
    super.addEdge(a, b)
    super.addEdge(b, a)
  }
}

object UGraph {
  def apply[A:Ordering](): UGraph[A] = new UGraph[A]()
}
