package graph

import scala.collection.mutable
import scala.collection.mutable.ArrayBuffer
import scala.math.Ordered._

case class Node(label: String) extends Ordered[Node] {
  def compare(that: Node) = this.label compare that.label
}

object Node {
  implicit def toNode(label: String) = Node(label)
}

case class GNode[A:Ordering](label: A) extends Ordered[GNode[A]] {
  override def compare(that: GNode[A]): Int = this.label compare that.label
}

object GNode {
  implicit def toNode[A:Ordering](label: A) = GNode[A](label)
}

// graph is a map of nodes to lists of nodes
class Graph extends mutable.HashMap[Node, scala.collection.mutable.Set[Node]] {
  def addNode(n: Node): Unit = {
    if (this.contains(n)) {
      throw new IllegalStateException("node already in graph")
    }
    else {
      this += (n -> mutable.Set[Node]())
    }
  }

  def addNodes(n: Node*): Unit = {
    for (elem <- n) {
      this.addNode(elem)
    }
  }

  def addEdge(a: Node, b: Node): Unit = {
    if (!this.contains(a)) throw new IllegalStateException(s"node $a not in graph")
    if (!this.contains(b)) throw new IllegalStateException(s"node $b not in graph")

    this (a).add(b)
  }

  def dfs(startHere: Node): Array[String] = {
    // non-recursive implementation
    require(this.contains(startHere))

    var visited = mutable.HashSet[Node]()
    var stack = mutable.Stack[Node]()
    var result_buffer = ArrayBuffer[Node]()

    stack.push(startHere)
    visited.add(startHere)
    result_buffer += startHere

    def next_unvisited_neighbor(n: Node): Option[Node] = {
      var adj_list = this (n).toList.sorted
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

    result_buffer.map(x => x.label).toArray
  }

  def bfs(startHere: Node): Array[String] = {
    require(this.contains(startHere))

    // use a Vector as a deque
    var deque = Vector[Node]()
    var visited = mutable.HashSet[Node]()

    deque = deque :+ startHere
    visited.add(startHere)
    var result_buffer = ArrayBuffer[Node]()

    while (!deque.isEmpty) {
      val front: Node = deque.take(1)(0)
      deque = deque.drop(1)
      result_buffer += front

      // enqueue all unvisited adj_list
      val adj_list = this(front).toList.sorted
      val unvisited = adj_list.filterNot(visited.contains(_))
      deque ++= unvisited
      visited ++= unvisited
    }
    result_buffer.map(x => x.label).toArray
  }
}

class UGraph extends Graph {
  // undirected graph
  override def addEdge(a: Node, b: Node): Unit = {
    super.addEdge(a, b)
    super.addEdge(b, a)
  }
}

object Graph {
  def apply(): Graph = new Graph()
}

object UGraph {
  def apply(): UGraph = new UGraph()
}
