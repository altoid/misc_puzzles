package tree

import org.scalatest.FunSuite
import roman.RomanNumeral

class TreeTest extends FunSuite {
  test("single node") {
    val root: tree.Tree[String] = "root"
    val l = root.children(0)
    assert(l === None)
    val s = l match {
      case Some(n: Tree[String]) => n.value
      case None => "nada"
    }
    assert(s === "nada")
  }

  test("assignment") {
    val root: tree.Tree[String] = "root"
    val r: tree.Tree[String] = "rightchild"

    root.children(1) = Some(r)

  }
}
