package exactcover

import scala.collection.mutable.ArrayBuffer

class Element {
  var u = this
  var d = this
  var l = this
  var r = this
}

class ColumnHeader(val name: String) extends Element {
  var count = 0  // number of bits in the column

  def empty: Boolean = this == this.d
}

// RowHeader objects are just an aid in navigation; nothing in the matrix points to them.
class RowHeader extends Element

case class Bit(columnheader: ColumnHeader) extends Element

class Matrix {
  val root = new ColumnHeader("__root__")
  var ncolumns = 0
  var rowheaders = new ArrayBuffer[RowHeader]()

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

  def addColumns(name: String*): Unit = {
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

    val rheader = new RowHeader
    var ccursor = root.r match {
      case ch: ColumnHeader => ch
      case _ => throw new ClassCastException
    }
    var last_item_inserted: Option[Bit] = None
    for (b <- bits) {
      b match {
        case '0' => {}
        case '1' => {
          val newbit = new Bit(ccursor)
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
            case None => {}
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
      case None => {}
    }

    rowheaders = rowheaders :+ rheader
  }

  private def displayRow(rheader: RowHeader): Unit = {
    var h: ColumnHeader = root.r match {
      case ch: ColumnHeader => ch
      case _ => throw new ClassCastException
    }

    var data: Option[Bit] = rheader.r match {
      case b: Bit => Some(b)
      case _ => None
    }

    while (h != root) {
      data = data match {
        case None => {
          print("0 ")
          None
        }
        case Some(b: Bit) => {
          if (b.columnheader == h) {
            print("1 ")
            b.r match {
              case n: Bit => Some(n)
              case _ => None
            }
          }
          else {
            print("0 ")
            data
          }
        }
      }

      h = h.r match {
        case ch: ColumnHeader => ch
        case _ => throw new ClassCastException
      }
    }
    println()
  }

  def display(): Unit = {
    // display column headers
    var h: ColumnHeader = root.r match {
      case ch: ColumnHeader => ch
      case _ => throw new ClassCastException
    }
    while (h != root) {
      print(h.name + " ")
      h = h.r match {
        case ch: ColumnHeader => ch
        case _ => throw new ClassCastException
      }
    }
    println()

    rowheaders.map(displayRow(_))
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
      uncover(nextbit.columnheader)
      nextbit = nextbit.l match {
        case x: Bit => x
        case _ => throw new ClassCastException
      }
    }
  }
}

class DLXAlgorithm(val matrix: Matrix) {

  var partial_solutions = List[Element]()

  // returns the shortest column encountered in traversing the colums left to right.
  // (knuth's S heuristic.)
  def shortest(): Option[ColumnHeader] = {
    var ch: ColumnHeader = matrix.root.r match {
      case x: ColumnHeader => x
      case _ => throw new ClassCastException
    }

    if (ch == matrix.root) return None

    var result: Option[ColumnHeader] = Some(ch)
    var mincount = ch.count

    while (ch != matrix.root) {
      if (ch.count < mincount) {
        mincount = ch.count
        result = Some(ch)
      }
      ch = ch.r match {
        case x: ColumnHeader => x
        case _ => throw new ClassCastException
      }
    }
    result
  }

  def dlx(level: Int = 0): Boolean = {
    if (matrix.empty()) {
      println(s"solution exists at level $level")
      return true
    }

    // check for an empty column.  if we find one, game over
    var h: ColumnHeader = matrix.root.r match {
      case x: ColumnHeader => x
      case _ => throw new ClassCastException
    }

    while (h != matrix.root) {
      if (h.empty) return false

      h = h.r match {
        case x: ColumnHeader => x
        case _ => throw new ClassCastException
      }
    }

    var o_nextch = shortest()
    while (o_nextch != None) {
      val nextch = o_nextch match {
        case Some(ch) => ch
      }

      matrix.cover(nextch)

      // go through each row and reduce
      var cvalue = nextch.d

      while (cvalue != nextch) {

        val bvalue = cvalue match {
          case x: Bit => x
          case _ => throw new ClassCastException
        }
        matrix.reduce_by_row(bvalue)

        partial_solutions = cvalue :: partial_solutions

        dlx(level + 1)

        partial_solutions = partial_solutions.tail

        matrix.unreduce_by_row(bvalue)
        cvalue = cvalue.d
      }
      matrix.uncover(nextch)

      o_nextch = shortest()
    }
    false
  }

}