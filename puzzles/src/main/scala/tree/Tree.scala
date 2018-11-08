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

  private def replace(node: Node[A], new_value: A): Unit = {
    // we can't change the value of a node, so we have to replace the node.
    val new_node: Node[A] = new_value

    new_node.parent = node.parent
    new_node.children(0) = node.children(0)
    new_node.children(1) = node.children(1)

    node.parent match {
      case Some(p) => {
        if (p.children(0) == node) {
          p.children(0) = Some(new_node)
        }
        else {
          p.children(1) = Some(new_node)
        }
      }
    }

    node.children(0) match {
      case Some(c) => c.parent = Some(new_node)
    }

    node.children(1) match {
      case Some(c) => c.parent = Some(new_node)
    }

    node.parent = None
    node.children(0) = None
    node.children(1) = None
  }

  private def replace_in_parent(node: Node[A], replacement: Option[Node[A]]): Unit = {
    val parent = node.parent

    parent match {
      case None => {
        root = replacement
      }
      case Some(p) => {
        if (p.children(0) == Some(node)) {
          p.children(0) = replacement
        }
        else {
          p.children(1) = replacement
        }
      }
    }

    replacement match {
      case Some(r) => r.parent = parent
      case None => ()
    }

    node.parent = None
    node.children(0) = None
    node.children(1) = None
  }

  def deleteValue(v: A): Unit = {
    def helper(subtree: Node[A], v: A): Unit = {
      if (v < subtree.value) {
        subtree.children(0) match {
          case Some(c) => helper(c, v)
          case None => return
        }
      }
      else if (v > subtree.value) {
        subtree.children(1) match {
          case Some(c) => helper(c, v)
          case None => return
        }
      }
      else {
        if (subtree.children(0) == None && subtree.children(1) == None) {
          replace_in_parent(subtree, None)
        }
        else if (subtree.children(0) != None && subtree.children(1) != None) {
          val succ = successor_node(subtree.value)

          succ match {
            // case None won't happen because subtree has a right child
            case Some(s) => {
              deleteValue(s.value)
              replace(subtree, s.value)
            }
          }
        }
        else if (subtree.children(0) != None) {
          replace_in_parent(subtree, subtree.children(0))
        }
        else {
          replace_in_parent(subtree, subtree.children(1))
        }
      }
    }

    root match {
      case Some(n) => helper(n, v)
      case None => ()
    }
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

  @tailrec
  private def subtree_min(node: Node[A]): Option[Node[A]] = {
    // give me the node holding the mininum value rooted at this subtree.
    node.children(0) match {
      case None => Some(node)
      case Some(n) => subtree_min(n)
    }
  }

  def successor(v: A): Option[A] = {
    successor_node(v) match {
      case None => None
      case Some(n) => Some(n.value)
    }
  }

  def successor_node(v: A): Option[Node[A]] = {
    // get the min in the right subtree

    val loc = locus(v)
    loc match {
      case None => None
      case Some(n) => {
        n.children(1) match {
          case None => None
          case Some(c) => subtree_min(c)
        }
      }
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

  def preorder(): List[A] = {
    def helper(acc: List[A], node: Option[Node[A]]): List[A] = {
      node match {
        case None => acc
        case Some(n) => {
          val l1 = n.value :: acc
          val l2 = helper(l1, n.children(0))
          val l3 = helper(l2, n.children(1))
          l3
        }
      }
    }

    helper(List[A](), root).reverse
  }
}