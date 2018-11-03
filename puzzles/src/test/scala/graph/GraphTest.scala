package graph

import graph.{Graph, Node}
import org.scalatest.FunSuite
// import scala.math.Ordered._

class GNodeTest extends FunSuite {
  test("cmp") {
    val c: Node[String] = Node("three")
    val d: Node[String] = Node("four")
    val e: Node[String] = Node("six")
    val f: Node[String] = Node("five")

    assert(d != e)
    assert(d < c)

    var l = List(c,d,e,f).sorted
    assert(l === List(f, d, e, c))
  }
}

class GraphTest extends FunSuite {
  test("graph - addNode") {
    val g = Graph[String]()
    val n = Node[String]("3")
    g.addNode(n)
    assertThrows[IllegalStateException] {
      g.addNode(n)
    }
    g.addNode(Node("4"))
  }

  test("graph - addNodes") {
    val g = Graph[String]()
    val n1 = Node("1")
    val n2 = Node("2")
    val n3 = Node("3")
    g.addNodes(n1, n2, n3)
    assert(g.contains(Node("3")))
  }

  test("graph - addEdge") {
    val g = Graph[String]()

    val n1 = Node("1")
    val n2 = Node("2")
    val n3 = Node("3")

    assertThrows[IllegalStateException] {
      g.addEdge(n2, n3)
    }
    g.addNode(n2)
    assertThrows[IllegalStateException] {
      g.addEdge(n2, n3)
    }
    g.addNode(n3)
    g.addEdge(n2, n3)

    assert(g(n2).contains(n3))
  }

  test("dfs") {
    val gr = UGraph[String]()

    val a: Node[String] = Node("a")
    val b: Node[String] = Node("b")
    val c: Node[String] = Node("c")
    val d: Node[String] = Node("d")
    val e: Node[String] = Node("e")
    val f: Node[String] = Node("f")
    val g: Node[String] = Node("g")
    val h: Node[String] = Node("h")

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

    val outsider: Node[String] = Node("mr_lonely")

    assertThrows[IllegalArgumentException] {
      gr.dfs(outsider)
    }

    var result = gr.dfs(a).mkString
    assert(result == "abegfchd")
  }

  test("bfs") {
    val gr = UGraph[String]()

    val a: Node[String] = Node("a")
    val b: Node[String] = Node("b")
    val c: Node[String] = Node("c")
    val d: Node[String] = Node("d")
    val e: Node[String] = Node("e")
    val f: Node[String] = Node("f")
    val g: Node[String] = Node("g")
    val h: Node[String] = Node("h")

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

    val outsider: Node[String] = Node("mr_lonely")

    assertThrows[IllegalArgumentException] {
      gr.dfs(outsider)
    }

    var result = gr.bfs(a).mkString
    assert(result == "abdgefch")
  }
}
