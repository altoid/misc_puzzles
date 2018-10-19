import scala.annotation.tailrec

object Misc {
  def genX(): IndexedSeq[Int] = {
    for {
      p <- (4 to 9)
      if (p % 2 == 0)
    } yield p
  }

  def combinations[A](n: Int, l: List[A]): List[List[A]] = {
    if (n > l.length) List[List[A]]()
    else if (n == 0 || l.length == 0) List(List[A]())
    else {
      val part1 = combinations(n - 1, l.tail).map(x => l.head :: x)
      val part2 = combinations(n, l.tail)
      part1 ++ part2
    }
  }

  /* given a list of integers, return the permutation of those integers that immediately follows it.  examples:

  (1 2 3 4) => (1 2 4 3)
  (2 4 3 1) => (3 1 2 4)
  (4 3 2 1) => Nil

   algorithm:
   - scan right-to-left to first item x that is smaller than
     the one to its right
   - swap it with the smallest item to the right
     of x that is larger than x (y)
   - sort the list [x+1:]
   */
  def successor[A](l: List[A]): List[A] = {
    def index_of_swap_candidate(i: Int): Int = {
      // scan right-to-left to first item x that is smaller than
      // the one to its right.  return -1 if this condition cannot be met.
      //
      // ********* do not call this if l.length < 2 *********
      //

      if (i < 0) -1
      else {
        if (l(i) < l(i + 1)) i
        else index_of_swap_candidate(i - 1)
      }
    }

    def index_of_least_greater_element_right_of(i: Int): Int = {
      if (i < 0) -1
      else if (i == l.length - 1) -1
      else {
        var j = i + 1
        var answer = j
        var m = l(j) // we know this is bigger than l(i)
        while (j < l.length) {
          if (l(i) < l(j) && l(j) < m) {
            m = l(j)
            answer = j
          }
          j += 1
        }
        answer
      }
    }

    val k = index_of_swap_candidate(l.length - 2)

    if (k < 0) Nil
    else {
      val x = index_of_least_greater_element_right_of(k)
      if (x < 0) Nil
      else {
        // create new list with elements at x and k swapped.  k < x
        val (a, b) = l.splitAt(k)
        val (c, d) = b.splitAt(x - k)

        val rest = (d.head :: c.tail) ::: (c.head :: d.tail)
        return a ::: (rest.head :: rest.tail.sorted)
      }
    }

    Nil
  }

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

  type RomanNumeral = String

  def romanToDecimal(r: RomanNumeral): Int = {
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

    helper(0, r.toList)
  }

  def main(args: Array[String]): Unit = {
//    successor(List(1, 2, 3, 4)) foreach println
//    successor(List(1, 2, 4, 3)) foreach println
//
//    successor(List(4, 3, 2, 1)) foreach println
//
    var l = List(1,2,3,4)
    while (l != Nil) {
      println(l)
      l = successor(l)
    }

    println(romanToDecimal("mdccclxxv")) // 1875
    println(romanToDecimal("mm"))
    println(romanToDecimal("mcm"))
    println(romanToDecimal("mc"))
    println(romanToDecimal("cm"))
    println(romanToDecimal("mmiii"))
    println(romanToDecimal("i"))
    println(romanToDecimal("v"))
    println(romanToDecimal("xii"))
  }

}
