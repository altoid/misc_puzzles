package boggle

import org.scalatest.FunSuite

class BoardTest extends FunSuite {
  ignore("basic") {
    assert(true)
  }

  ignore("generate board") {
    val board = new Board()
    board.display()
    println(Board.size)
  }

  ignore("cell test") {
    val cell = Cell('A')
    println(cell)

    val cell2: Cell = 'B'
    println(cell2)
  }

  ignore("dict test") {
    val board = new Board()
    if (board.all_words.nonEmpty) {
      println(board.all_words.head)
    }
  }

  ignore("prefixes") {
    val board = new Board()
    val matches = board.words_matching_prefix("a", board.all_words)
    println(matches.length)
    // matches.foreach(println(_))
  }

  ignore("delta") {
    for {
      dr <- -1 until 2
      dc <- -1 until 2 if dc != 0 || dr != 0
    } println(s"$dr, $dc")
  }

  ignore("play") {
    val board = new Board()

    board.play()
  }

  test("dislay results") {
    val nwords = 53
    val displayColumns = 6
    val nrows: Int = (nwords + (displayColumns - 1)) / displayColumns
    assert(nrows == 9)

    for (r <- 0 until nrows) {
      for (i <- r until nwords by nrows) {
        print(s"$i ")
      }
      println
    }
  }
}
