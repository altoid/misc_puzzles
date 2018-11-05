package tree

import scala.annotation.tailrec
import scala.math.Ordered._

class Tree[A:Ordering] {
  class Node[A:Ordering](val value: A, val nchildren: Int = 2) extends Ordered[Node[A]] {
    val children = Array.fill(nchildren)(None:Option[Node[A]])
    override def compare(that: Node[A]): Int = this.value compare that.value
  }

  object Node {
    implicit def toNode[A:Ordering](label: A) = Node[A](label)
    def apply[A:Ordering](label: A): Node[A] = new Node[A](label)
  }

  private var root: Option[Node[A]] = None

  def addValue(v: A): Unit = {
    // duplicate elements not allowed

    @tailrec
    def addValue_helper(node: Node[A], v: A): Unit = {
      if (v == node.value) return
      if (v < node.value) {
        node.children(0) match {
          case None => node.children(0) = Some(v)
          case Some(n) => addValue_helper(n, v)
        }
      }
      else {
        node.children(1) match {
          case None => node.children(1) = Some(v)
          case Some(n) => addValue_helper(n, v)
        }
      }
    }

    root match {
      case None => root = Some(v)
      case Some(n) => addValue_helper(n, v)
    }
  }

  def addValues(vals: A*): Unit = {
    for (v <- vals) {
      addValue(v)
    }
  }

  def deleteValue(v: A): Unit = {
    ???
  }

  def contains(v: A): Boolean = {
    @tailrec
    def contains_helper(node: Option[Node[A]], v: A): Boolean = {
      node match {
        case Some(n) => {
          if (n.value == v) true
          else if (v < n.value) {
            contains_helper(n.children(0), v)
          }
          else contains_helper(n.children(1), v)
        }
        case None => false
      }
    }

    contains_helper(root, v)
  }

  def height(): Int = {
    def height_helper(node: Option[Node[A]]): Int = {
      node match {
        case None => 0
        case Some(n) => 1 + math.max(height_helper(n.children(0)), height_helper(n.children(1)))
      }
    }

    height_helper(root)
  }

  def size(): Int = {
    def size_helper(node: Option[Node[A]]): Int = {
      node match {
        case None => 0
        case Some(n) => 1 + size_helper(n.children(0)) + size_helper(n.children(1))
      }
    }

    size_helper(root)
  }

  def min(): A = {
    require(size() > 0)

    def min_helper(node: Node[A]): A = {
      node.children(0) match {
        case None => node.value
        case Some(n) => min_helper(n)
      }
    }

    root match {
      case Some(n) => min_helper(n)
    }
  }

  def max(): A = {
    require(size() > 0)

    def max_helper(node: Node[A]): A = {
      node.children(1) match {
        case None => node.value
        case Some(n) => max_helper(n)
      }
    }

    root match {
      case Some(n) => max_helper(n)
    }
  }
}