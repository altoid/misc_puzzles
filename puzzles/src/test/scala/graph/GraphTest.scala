package graph

import graph.{Graph, Node}
import org.scalatest.FunSuite

class GraphTest extends FunSuite {
  test("node") {
    val n = Node(4)
    val m: Node[Int] = 4
    assert(n.data == m.data)
  }

  test("node cmp") {
    val o_int = implicitly[Ordering[Node[Int]]]
    val o_str = implicitly[Ordering[Node[String]]]

    val a: Node[Int] = 3
    val b: Node[Int] = 4
    assert(o_int.lt(a, b))

    val c: Node[String] = "three"
    val d: Node[String] = "four"
    val e: Node[String] = "four"
    assert(o_str.lt(d, c))

    assert(o_str.compare(d, e) == 0)
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
    g.addNodes(1, 2, 3)
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

  test("dfs") {
    // cf. https://www.youtube.com/watch?v=zLZhSSXAwxI

    val gr = UGraph[String]()

    val a: Node[String] = "a"
    val b: Node[String] = "b"
    val c: Node[String] = "c"
    val d: Node[String] = "d"
    val e: Node[String] = "e"
    val f: Node[String] = "f"
    val g: Node[String] = "g"
    val h: Node[String] = "h"

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

    val outsider: Node[String] = "mr_lonely"

    assertThrows[NoSuchElementException] {
      gr.dfs(outsider)
    }

    var result = gr.dfs(a)
    result foreach println
  }
}
