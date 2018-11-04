package tree

import scala.math.Ordered._

class Tree[A](val value: A, val nchildren: Int = 2) {
  val children = Array.fill(nchildren)(None:Option[Tree[A]])
}

object Tree {
  implicit def toNode[A](label: A) = Tree[A](label)
  def apply[A](label: A): Tree[A] = new Tree[A](label)
}
