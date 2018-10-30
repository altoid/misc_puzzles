package graph

import scala.collection.mutable
//import collection.mutable.{HashMap,Set}

case class Node[A](data: A)

object Node {
  implicit def toNode[A](data: A) = Node(data)
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
}

object Graph {
  def apply[A](): Graph[A] = new Graph[A]()
}
