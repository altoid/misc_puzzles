package graph

import org.scalatest.FunSuite
import roman.RomanNumeral

class GNodeTest extends FunSuite {
  test("cmp") {
    val c: Node[String] = "three"
    val d: Node[String] = "four"
    val e: Node[String] = "six"
    val f: Node[String] = "five"

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
    g.addNode("4")
  }

  test("graph - addNodes") {
    val g = Graph[String]()
    g.addNodes("1", "2", "3")
    assert(g.contains("3"))
  }

  test("graph - addEdge") {
    val g = Graph[String]()

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

    val outsider: Node[String] = Node("mr_lonely")

    assertThrows[IllegalArgumentException] {
      gr.dfs(outsider)
    }

    val result = gr.dfs(a).mkString
    assert(result == "abegfchd")
  }

  test("dfs - roman numerals") {
    val gr = UGraph[RomanNumeral]()

    val a: Node[RomanNumeral] = RomanNumeral("i")
    val b: Node[RomanNumeral] = RomanNumeral("iii")
    val c: Node[RomanNumeral] = RomanNumeral("v")
    val d: Node[RomanNumeral] = RomanNumeral("vii")
    val e: Node[RomanNumeral] = RomanNumeral("ix")
    val f: Node[RomanNumeral] = RomanNumeral("xi")
    val g: Node[RomanNumeral] = RomanNumeral("xiii")
    val h: Node[RomanNumeral] = RomanNumeral("xv")

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

    val result = gr.dfs(a).mkString(" ")
    assert(result == "i iii ix xiii xi v xv vii")
  }

  test("bfs") {
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

    val outsider: Node[String] = Node("mr_lonely")

    assertThrows[IllegalArgumentException] {
      gr.dfs(outsider)
    }

    val result = gr.bfs(a).mkString
    assert(result == "abdgefch")
  }

  test("bipartite") {
    val gr = UGraph[String]()

    val a: Node[String] = "a"
    val b: Node[String] = "b"
    val c: Node[String] = "c"
    val d: Node[String] = "d"

    gr.addNodes(a, b, c, d)

    gr.addEdge(a, b)
    gr.addEdge(b, c)
    gr.addEdge(c, d)
    gr.addEdge(d, a)

    /*
      a ----- b
      |       |
      |       |
      d ----- c
     */

    assert(gr.isBipartite())

    gr.addEdge(a, c)

    assert(!gr.isBipartite())
  }
}
