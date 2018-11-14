package exactcover

import scala.collection.mutable.ArrayBuffer

class Element {
  var u = this
  var d = this
  var l = this
  var r = this
}

class ColumnHeader(val name: String) extends Element

class RowHeader extends Element

class Bit(rowheader: RowHeader, columnheader: ColumnHeader) extends Element

class Matrix {
  val root = new ColumnHeader("__root__")

  def addColumn(name: String): Unit = {
    // no requirement that column names be unique
    val ch = new ColumnHeader(name)
    root.l.r = ch
    ch.r = root
    ch.l = root.l
    root.l = ch
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
}
