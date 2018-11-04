package tree

import org.scalatest.FunSuite
import roman.RomanNumeral

class TreeTest extends FunSuite {
  ignore("cmp") {
    val c: tree.Tree[String] = "three"
    val d: tree.Tree[String] = "four"
    val e: tree.Tree[String] = "six"
    val f: tree.Tree[String] = "five"

    assert(d != e)
    assert(d < c)

    var l = List(c,d,e,f).sorted
    assert(l === List(f, d, e, c))
  }

  test("single node") {
    val root: tree.Tree[String] = "root"
    val l = root.children(0)
    println(l)
    val s = l match {
      case Some(n: Tree[String]) => n.value
      case None => "nada"
    }
    println(s)
  }
}
