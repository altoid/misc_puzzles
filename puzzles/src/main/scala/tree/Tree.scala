package tree

import scala.annotation.tailrec
import scala.math.Ordered._

class Tree[A] {
  class Node[A](val value: A, val nchildren: Int = 2) {
    val children = Array.fill(nchildren)(None:Option[Node[A]])
  }

  object Node {
    implicit def toNode[A](label: A) = Node[A](label)
    def apply[A](label: A): Node[A] = new Node[A](label)
  }

  private var root: Option[Node[A]] = None

  def addValue(v: A): Unit = {
    // duplicate elements not allowed

    @tailrec
    def addValue_helper(node: Node[A], v: A): Unit = {
      if (v == node.value) return
      if (v.hashCode() < node.value.hashCode()) {
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

  def deleteValue(v: A): Unit = {
    ???
  }

  def contains(v: A): Boolean = {
    @tailrec
    def contains_helper(node: Option[Node[A]], v: A): Boolean = {
      node match {
        case Some(n) => {
          if (n.value == v) true
          else if (v.hashCode() < n.value.hashCode()) {
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
}