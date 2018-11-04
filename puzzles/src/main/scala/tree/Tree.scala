package tree

import scala.math.Ordered._

class Tree[A:Ordering](val value: A, val nchildren: Int = 2) extends Ordered[Tree[A]] {
  override def compare(that: Tree[A]): Int = this.value compare that.value

  val children = Array.fill(nchildren)(None:Option[Tree[A]])
}

object Tree {
  implicit def toNode[A:Ordering](label: A) = Tree[A](label)
  implicit def ord[A:Ordering]: Ordering[Tree[A]] = Ordering.by(_.value)
  def apply[A:Ordering](label: A): Tree[A] = new Tree[A](label)
}
