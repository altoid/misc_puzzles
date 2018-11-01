package graph

import scala.collection.mutable
import scala.collection.mutable.ArrayBuffer

case class Node(label: String)

object Node {
  implicit def toNode(label: String) = Node(label)
  implicit def orderByLabel: Ordering[Node] = Ordering.by(_.label)
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
    for (elem <- n) { this.addNode(elem) }
  }

  def addEdge(a: Node, b: Node): Unit = {
    if (!this.contains(a)) throw new IllegalStateException(s"node $a not in graph")
    if (!this.contains(b)) throw new IllegalStateException(s"node $b not in graph")

    this(a).add(b)
  }

  def dfs(startHere: Node): Array[String] = {
    if (!this.contains(startHere)) throw new NoSuchElementException(s"node $startHere is not in the graph")


    var visited = mutable.HashSet[Node]()
    var stack = mutable.Stack[Node]()

    var result_buffer = ArrayBuffer[Node]()
    stack.push(startHere)
    result_buffer += startHere

    def next_unvisited_neighbor(n: Node): Option[Node] = {
      var adj_list = this(n).toList.sortWith(_.label < _.label)
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
