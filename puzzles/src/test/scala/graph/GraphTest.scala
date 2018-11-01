package graph

import graph.{Graph, Node}
import org.scalatest.FunSuite

class GraphTest extends FunSuite {
  test("node cmp") {
    val c: Node = "three"
    val d: Node = "four"
    val e: Node = "four"

    assert(d == e)

    val ordering = implicitly[Ordering[Node]]

    assert(ordering.lt(d, c))
  }

  test("graph - addNode") {
    val g = Graph()
    val n = Node("3")
    g.addNode(n)
    assertThrows[IllegalStateException] {
      g.addNode(n)
    }
    g.addNode("4")
  }

  test("graph - addNodes") {
    val g = Graph()
    g.addNodes("1", "2", "3")
    assert(g.contains("3"))
  }

  test("graph - addEdge") {
    val g = Graph()

    assertThrows[IllegalStateException] {
      g.addEdge("2", "3")
    }
    g.addNode("2")
    assertThrows[IllegalStateException] {
      g.addEdge("2", "3")
    }
    g.addNode("3")
    g.addEdge("2", "3")

    assert(g("2").contains("3"))
  }

  test("dfs") {
    // cf. https://www.youtube.com/watch?v=zLZhSSXAwxI

    val gr = UGraph()

    val a: Node = "a"
    val b: Node = "b"
    val c: Node = "c"
    val d: Node = "d"
    val e: Node = "e"
    val f: Node = "f"
    val g: Node = "g"
    val h: Node = "h"

    gr.addNodes(a, b, c, d, e, f, g, h)

    gr.addEdge(a, b)
    gr.addEdge(a, g)
    gr.addEdge(a, d)

    gr.addEdge(b, e)
    gr.addEdge(b, f)

    gr.addEdge(c, f)
    gr.addEdge(c, h)

    gr.addEdge(d, f)

    gr.addEdge(e, g)

    val outsider: Node = "mr_lonely"

    assertThrows[NoSuchElementException] {
      gr.dfs(outsider)
    }

    var result = gr.dfs(a).mkString
    assert(result == "abegfchd")
  }
}
