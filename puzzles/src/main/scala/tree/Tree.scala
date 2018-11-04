package tree

import scala.math.Ordered._

abstract class Tree[+A] {
}

case class Node[+A](value: A, l: Tree[A], r: Tree[A]) extends Tree[A]
case class Leaf[+A](value: A) extends Tree[A]
case object Empty extends Tree[Nothing]



//object Tree {
//  implicit def toNode[A](label: A) = Tree[A](label, None:Option[Tree[A]], None:Option[Tree[A]])
//  def apply[A](label: A, l: Option[Tree[A]], r: Option[Tree[A]]): Tree[A] = new Tree[A](label, l, r)
//}
