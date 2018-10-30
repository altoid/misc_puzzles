package graph

import scala.collection.mutable
//import collection.mutable.{HashMap,Set}

case class Node[A](data: A)

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
}
