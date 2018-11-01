package graph

import scala.collection.mutable
import scala.collection.mutable.ArrayBuffer

case class Node[A](data: A) extends Ordered[A] {
  def compareTo(that: Node[A]): Int = this.data compare that.data
}

object Node {
  implicit def toNode[A](data: A) = Node(data)
  implicit def intOrdering: Ordering[Node[Int]] = Ordering.by(n => n.data)
  implicit def strOrdering: Ordering[Node[String]] = Ordering.by(n => n.data)
}

// graph is a map of nodes to lists of nodes
class Graph[A] extends mutable.HashMap[Node[A], scala.collection.mutable.Set[Node[A]]] {
  def addNode(n: Node[A]): Unit = {
    if (this.contains(n)) {
      throw new IllegalStateException("node already in graph")
    }
    else {
      this += (n -> mutable.Set[Node[A]]())
    }
  }

  def addNodes(n: Node[A]*): Unit = {
    for (elem <- n) { this.addNode(elem) }
  }

  def addEdge(a: Node[A], b: Node[A]): Unit = {
    if (!this.contains(a)) throw new IllegalStateException(s"node $a not in graph")
    if (!this.contains(b)) throw new IllegalStateException(s"node $b not in graph")

    this(a).add(b)
  }

  def dfs(startHere: Node[A]): Array[A] = {
    if (!this.contains(startHere)) throw new NoSuchElementException(s"node $startHere is not in the graph")

    var result_buffer = ArrayBuffer[Node[A]]()

    var visited = mutable.HashSet[Node[A]]()

    var stack = mutable.Stack[Node[A]]()
    stack.push(startHere)
    result_buffer += startHere

    def next_unvisited_neighbor(n: Node[A]): Option[Node[A]] = {
      val ordering = implicitly[Ordering[Node[A]]]
      var adj_list = this(n).toList.sortWith(ordering.lt(_, _))
      adj_list.filterNot(x => visited.contains(x)).headOption
    }

    while (!stack.isEmpty) {
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

    var result = result_buffer.map(x => x.data).toArray
    result
  }
}

class UGraph[A] extends Graph[A] {
  // undirected graph
  override def addEdge(a: Node[A], b: Node[A]): Unit = {
    super.addEdge(a, b)
    super.addEdge(b, a)
  }
}

object Graph {
  def apply[A](): Graph[A] = new Graph[A]()
}

object UGraph {
  def apply[A](): UGraph[A] = new UGraph[A]()
}
