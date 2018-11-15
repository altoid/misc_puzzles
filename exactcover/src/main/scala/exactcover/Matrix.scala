package exactcover

import scala.collection.mutable.ArrayBuffer

class Element {
  var u = this
  var d = this
  var l = this
  var r = this
}

class ColumnHeader(val name: String) extends Element

// RowHeader objects are just an aid in navigation; nothing in the matrix points to them.
class RowHeader extends Element

class Bit(rowheader: RowHeader, columnheader: ColumnHeader) extends Element

class Matrix {
  val root = new ColumnHeader("__root__")
  var ncolumns = 0
  var rowheaders = new ArrayBuffer[RowHeader]()

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
    if (bits.length != ncolumns) throw new IllegalStateException(s"bit vector has $bits.length bits but matrix has $ncolumns columns")

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
          val newbit = new Bit(rheader, ccursor)
          ccursor.u.d = newbit
          newbit.d = ccursor
          newbit.u = ccursor.u
          ccursor.u = newbit
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
      }
    }
  }
}
