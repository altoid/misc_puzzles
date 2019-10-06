package roman

import scala.annotation.tailrec

/*
i ii iii iv v vi vii viii ix x
xi
xxi
xxxi
xli
li
lxi
lxxi
lxxxi
xci
ci cii ciii civ
cx

digits:  i v x l c d m
if a digit immediately precedes a larger digit, smaller is subtracted from larger
only i, x, and c are used as subtractors
there is never more than 1 subtractor
i - v, x
x - l, c
c - d, m

won't ever have vv or dd

1965 = mcmlxv
2000 = mm
1900 = mcm
1100 = mc
900 = cm
400 = cd
 */

class RomanNumeral(val roman: String) {

  def toInt(): Int = {
    // works for roman numbers that are correct, but doesn't check for invalid ones - permits iiimmm
    // would have to add succession rules:
    // i - x, v, i
    // v - anything smaller
    // x - x, v, i, l, c
    // l - anything smaller
    // c - anything
    // d - anything smaller
    // m - anything
    //
    // these rules still permit cmmm
    // for now, fuck it

    @tailrec
    def helper(acc: Int, arr: List[Char]): Int = {
      arr match {
        case 'i' :: 'v' :: rest => helper(4 + acc, rest)
        case 'i' :: 'x' :: rest => helper(9 + acc, rest)
        case 'i' :: rest => helper(1 + acc, rest)
        case 'v' :: rest => helper(5 + acc, rest)
        case 'x' :: 'l' :: rest => helper(40 + acc, rest)
        case 'x' :: 'c' :: rest => helper(90 + acc, rest)
        case 'x' :: rest => helper(10 + acc, rest)
        case 'l' :: rest => helper(50 + acc, rest)
        case 'c' :: 'd' :: rest => helper(400 + acc, rest)
        case 'c' :: 'm' :: rest => helper(900 + acc, rest)
        case 'c' :: rest => helper(100 + acc, rest)
        case 'd' :: rest => helper(500 + acc, rest)
        case 'm' :: rest => helper(1000 + acc, rest)
        case Nil => acc
      }
    }

    helper(0, roman.toList)
  }

  override def toString: String = roman
}

object RomanNumeral {
  implicit def orderByValue: Ordering[RomanNumeral] = Ordering.by(r => r.toInt())

  def apply(roman: String): RomanNumeral = new RomanNumeral(roman)
}

