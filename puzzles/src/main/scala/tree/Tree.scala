package tree

import scala.annotation.tailrec
import scala.math.Ordered._

class Tree[A:Ordering] {
  class Node[A:Ordering](val value: A, val nchildren: Int = 2) extends Ordered[Node[A]] {
    val children = Array.fill(nchildren)(None:Option[Node[A]])
    var parent: Option[Node[A]] = None
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
          case None => {
            val child: Node[A] = v
            child.parent = Some(node)
            node.children(0) = Some(child)
          }
          case Some(n) => addValue_helper(n, v)
        }
      }
      else {
        node.children(1) match {
          case None => {
            val child: Node[A] = v
            child.parent = Some(node)
            node.children(1) = Some(child)
          }
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

  def locus(v: A): Option[Node[A]] = {
    // return the node containing v, or None
    @tailrec
    def helper(node: Option[Node[A]], v: A): Option[Node[A]] = {
      node match {
        case None => None
        case Some(n) => {
          if (n.value == v) Some(n)
          else if (v < n.value) helper(n.children(0), v)
          else helper(n.children(1), v)
        }
      }
    }

    helper(root, v)
  }

  def contains(v: A): Boolean = {
    val loc = locus(v)
    loc match {
      case None => false
      case Some(n) => true
    }
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

  def successor(v: A): Option[Node[A]] = {
    // get the min in the right subtree

    @tailrec
    def helper(node: Node[A]): Option[Node[A]] = {
      node.children(0) match {
        case None => Some(node)
        case Some(n) => helper(n)
      }
    }

    val loc = locus(v)
    loc match {
      case None => None
      case Some(n) => helper(n)
    }
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