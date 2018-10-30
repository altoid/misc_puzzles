package graph

import graph.{Graph,Node}
import org.scalatest.FunSuite

class GraphTest extends FunSuite {
  test("node") {
    val n = Node(3)
    println(s"$n")
    val m: Node[Int] = 4
    println(s"$m")
  }

  test("graph - addNode") {
    val g = Graph[Int]()
    val n = Node(3)
    g.addNode(n)
    assertThrows[IllegalStateException] {
      g.addNode(n)
    }
    g.addNode(4)
  }

  test("graph - addNodes") {
    val g = Graph[Int]()
    g.addNodes(1,2,3)
    assert(g.contains(3))
  }

  test("graph - addEdge") {
    val g = Graph[Int]()

    assertThrows[IllegalStateException] {
      g.addEdge(2, 3)
    }
    g.addNode(2)
    assertThrows[IllegalStateException] {
      g.addEdge(2, 3)
    }
    g.addNode(3)
    g.addEdge(2, 3)

    assert(g(2).contains(3))
  }
}
