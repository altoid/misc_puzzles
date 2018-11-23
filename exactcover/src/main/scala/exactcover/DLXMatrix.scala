package exactcover

import scala.collection.mutable
import scala.collection.mutable.ArrayBuffer

trait Element {
  var u: Element = this
  var d: Element = this
  var l: Element = this
  var r: Element = this
}

class ColumnHeader(val name: String) extends Element {
  var count = 0 // number of bits in the column

  def empty: Boolean = this == this.d

  override def toString = name
}

class RowHeader(val index: Int, val bits: String) extends Element {
  override def toString: String = bits
}

object RowHeader {
  implicit def ord: Ordering[RowHeader] = Ordering.by(_.index)
}

case class Bit(rowHeader: RowHeader, columnheader: ColumnHeader) extends Element

class DLXMatrix {
  val root = new ColumnHeader("__root__")
  var ncolumns = 0
  var rowheaders = new ArrayBuffer[RowHeader]()
  val bits2rowheaders = new mutable.HashMap[String, RowHeader]()

  def empty(): Boolean = root.r == root

  def addColumn(name: String): Unit = {
    // no requirement that column names be unique
    val ch = new ColumnHeader(name)
    root.l.r = ch
    ch.r = root
    ch.l = root.l
    root.l = ch
    ncolumns += 1
  }

  def addColumns(name: Seq[String]): Unit = {
    for (n <- name) {
      addColumn(n)
    }
  }

  def findColumn(name: String): Option[ColumnHeader] = {
    var h: ColumnHeader = root.r match {
      case ch: ColumnHeader => ch
      case _ => throw new ClassCastException
    }
    while (h != root) {
      if (h.name == name) return Some(h)
      h = h.r match {
        case ch: ColumnHeader => ch
        case _ => throw new ClassCastException
      }
    }
    None
  }

  def columnNames(): List[String] = {
    var buf = new ArrayBuffer[String]()

    var h: ColumnHeader = root.r match {
      case ch: ColumnHeader => ch
      case _ => throw new ClassCastException
    }
    while (h != root) {
      buf = buf :+ h.name
      h = h.r match {
        case ch: ColumnHeader => ch
        case _ => throw new ClassCastException
      }
    }
    buf.toList
  }

  def addRow(bits: String): Unit = {
    require(bits.length > 0)

    // bits is a string of 0s and 1s
    if (bits.length != ncolumns) {
      throw new IllegalStateException(s"bit vector has $bits.length bits but matrix has $ncolumns columns")
    }

    val rheader = new RowHeader(rowheaders.length, bits)
    var ccursor = root.r match {
      case ch: ColumnHeader => ch
      case _ => throw new ClassCastException
    }
    var last_item_inserted: Option[Bit] = None
    for (b <- bits) {
      b match {
        case '0' =>
        case '1' => {
          val newbit = Bit(rheader, ccursor)
          ccursor.u.d = newbit
          newbit.d = ccursor
          newbit.u = ccursor.u
          ccursor.u = newbit
          ccursor.count += 1

          last_item_inserted match {
            case Some(oldbit) => {
              newbit.l = oldbit
              newbit.r = oldbit.r
              oldbit.r.l = newbit
              oldbit.r = newbit
            }
            case None =>
          }
          last_item_inserted = Some(newbit)
        }
      }
      ccursor = ccursor.r match {
        case ch: ColumnHeader => ch
        case _ => throw new ClassCastException
      }
    }

    last_item_inserted match {
      case Some(b) => {
        rheader.r = b.r
        rheader.l = b
      }
      case None =>
    }

    bits2rowheaders += (bits -> rheader)

    rowheaders = rowheaders :+ rheader
  }

  private def displayRow(rheader: RowHeader): Unit = {
    println(rheader.bits.mkString(" "))
  }

  def display(subset: Option[Vector[RowHeader]] = None): Unit = {
    // display column headers
    println(s"$ncolumns columns")
    var h = root.r
    while (h != root) {
      print(h + " ")
      h = h.r
    }
    println()

    subset match {
      case None => rowheaders.map(displayRow(_))
      case Some(v: Vector[RowHeader]) => v.map(displayRow(_))
    }
    println()
  }

  def cover(columnHeader: ColumnHeader): Unit = {
    columnHeader.l.r = columnHeader.r
    columnHeader.r.l = columnHeader.l

    var cd = columnHeader.d

    while (cd != columnHeader) {
      var rd = cd.r match {
        case b: Bit => b
        case _ => throw new ClassCastException
      }

      while (rd != cd) {
        rd.d.u = rd.u
        rd.u.d = rd.d
        rd.columnheader.count -= 1
        rd = rd.r match {
          case b: Bit => b
          case _ => throw new ClassCastException
        }
      }
      cd = cd.d
    }
  }

  def uncover(columnHeader: ColumnHeader): Unit = {
    columnHeader.l.r = columnHeader
    columnHeader.r.l = columnHeader

    var cd = columnHeader.u
    while (cd != columnHeader) {
      var rd = cd.r match {
        case b: Bit => b
        case _ => throw new ClassCastException
      }

      while (rd != cd) {
        rd.d.u = rd
        rd.u.d = rd
        rd.columnheader.count += 1
        rd = rd.r match {
          case b: Bit => b
          case _ => throw new ClassCastException
        }
      }
      cd = cd.u
    }
  }

  def reduce_by_row(b: Bit): Unit = {
    // cover all the columns that the bits in this row are in.

    var nextbit = b.r match {
      case x: Bit => x
      case _ => throw new ClassCastException
    }

    while (nextbit != b) {
      // println("reduce_by_row:  covering " + nextbit.columnheader)
      cover(nextbit.columnheader)
      nextbit = nextbit.r match {
        case x: Bit => x
        case _ => throw new ClassCastException
      }
    }
  }

  def unreduce_by_row(b: Bit): Unit = {
    // cover all the columns that the bits in this row are in.

    var nextbit = b.l match {
      case x: Bit => x
      case _ => throw new ClassCastException
    }

    while (nextbit != b) {
      // println("unreduce_by_row:  uncovering " + nextbit.columnheader)
      uncover(nextbit.columnheader)
      nextbit = nextbit.l match {
        case x: Bit => x
        case _ => throw new ClassCastException
      }
    }
  }
}

class DLXAlgorithm(val matrix: DLXMatrix) {

  private var partial_solutions = List[RowHeader]()
  var solutions: mutable.Set[Vector[RowHeader]] = mutable.HashSet[Vector[RowHeader]]()
  private var _leaves = 0
  private var _nodes = 0

  def leaves = _leaves

  def nodes = _nodes

  private def reset(): Unit = {
    _leaves = 0
    _nodes = 0
    partial_solutions = Nil
    solutions.clear()
  }

  // the algorithm is written to gracefully terminate when 1 solution is found.  "gracefully terminate" means
  // that all of the covering steps that were done will be undone when dlx() returns.  note, however, that any
  // columns covered by initializing with a seed will remain covered.

  private def helper(heuristic: DLXMatrix => Option[ColumnHeader])(level: Int): Boolean = {
    if (matrix.empty()) {
      val solution: Vector[RowHeader] = partial_solutions.toArray.sorted.toVector
      solutions += solution
      _leaves += 1
      return true
    }

    _nodes += 1

    // check for an empty column.  if we find one, game over
    var h: ColumnHeader = matrix.root.r match {
      case x: ColumnHeader => x
      case _ => throw new ClassCastException
    }

    while (h != matrix.root) {
      if (h.empty) {
        return false
      }

      h = h.r match {
        case x: ColumnHeader => x
        case _ => throw new ClassCastException
      }
    }

    var found_solution = false
    val column_to_traverse = heuristic(matrix)
    column_to_traverse match {
      case None =>
      case Some(nextch) => {
        // println("    " * level + s"covering $nextch")
        matrix.cover(nextch)

        // go through each row and reduce
        var cvalue = nextch.d

        while (!found_solution && cvalue != nextch) {

          val bvalue = cvalue match {
            case x: Bit => x
            case _ => throw new ClassCastException
          }
          matrix.reduce_by_row(bvalue)

          partial_solutions = bvalue.rowHeader :: partial_solutions

          found_solution = helper(heuristic)(level + 1)

          partial_solutions = partial_solutions.tail

          matrix.unreduce_by_row(bvalue)
          cvalue = cvalue.d
        }
        // println("    " * level + s"uncovering $nextch")
        matrix.uncover(nextch)
        if (found_solution) {
          return found_solution
        }
      }
    }
    false
  }

  def dlx(heuristic: DLXMatrix => Option[ColumnHeader], opt_seeds: Option[Seq[String]] = None): Boolean = {
    // seeds is the set of rows (by number) that we want in a
    // solution.  it may be that the seed list precludes a solution
    // when one may be present in general.  tough shit.

    reset()

    opt_seeds match {
      case None =>
      case Some(seeds: Seq[String]) => {
        for (s <- seeds) {
          val rheader = matrix.bits2rowheaders(s)
          val rdata: Bit = rheader.r match {
            case b: Bit => b
            case _ => throw new ClassCastException
          }
          val cheader = rdata.columnheader
          matrix.cover(cheader)
          matrix.reduce_by_row(rdata)
        }
        partial_solutions = seeds.map(matrix.bits2rowheaders(_)).toList
      }
    }

    helper(heuristic)(0)
  }
}

object DLXMatrix {
  def shortestColumns(m: DLXMatrix): Option[ColumnHeader] = {
    var columns = ArrayBuffer[ColumnHeader]()

    var ch: ColumnHeader = m.root.r match {
      case x: ColumnHeader => x
      case _ => throw new ClassCastException
    }

    var mincount = ch.count
    var shortest = ch

    while (ch != m.root) {
      if (ch.count < mincount) {
        mincount = ch.count
        shortest = ch
      }
      ch = ch.r match {
        case x: ColumnHeader => x
        case _ => throw new ClassCastException
      }
    }

    if (shortest != m.root) Some(shortest)
    else None
  }

  def leftMost(m: DLXMatrix): Option[ColumnHeader] = {
    var columns = ArrayBuffer[ColumnHeader]()

    val ch: ColumnHeader = m.root.r match {
      case x: ColumnHeader => x
      case _ => throw new ClassCastException
    }

    if (ch != m.root) Some(ch)
    else None
  }
}