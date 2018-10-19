object Puzzles99 extends App {

  // puzzle # 2
  def penultimate[A](l: List[A]): A = {
    l match {
      // for this case, we have a head element and a tail that is a singleton list.  ana2 is one element of type A.
      case a1 :: List(ana2) => a1
      case _ :: rest => penultimate(rest)
      case _ => throw new IllegalArgumentException("fml")
    }
  }

  // puzzle # 5 - reverse a list
  def esrever[A](l: List[A]): List[A] = {
    (l foldLeft List[A]())((b, a) => a :: b)
  }

  // puzzle # 6
  def isPalindrome[A](l: List[A]): Boolean = {
    // the purpose of counter is to keep us from traversing all of the list.  with the counter, we can stop halfway
    // through.
    def helper(l1: List[A], l2: List[A], counter: Int): Boolean = {
      if (counter < 2) l1.head == l2.head
      else (l1.head == l2.head) && helper(l1.tail, l2.tail, counter - 2)
      // not tail-recursive
    }

    if (l.isEmpty) true
    else helper(l, l.reverse, l.length)
  }

  val list1 = List(1, 2, 4)

  val p = penultimate(list1)
  // println(p)

  val list2 = List(1, 2, 3, 4, 4, 3, 2, 1)
  println(isPalindrome(list2))
  val list3 = List(1, 2, 3, 4, 5, 4, 3, 2, 1)
  println(isPalindrome(list3))
  val singleton = List(1)
  println(isPalindrome(singleton))
  val empty = List()
  println(isPalindrome(empty))
  val list4 = List(1, 2, 3, 4, 5, 5, 3, 2, 1)
  println(isPalindrome(list4))

  val list5 = List('d', 'e', 's', 'r', 'e', 'v', 'e', 'r')
  println(esrever(list5).mkString)

  // problem 7 - flatten a list
  def fml(l: List[Any]): List[Any] = {
    l flatMap {
      case x: List[Any] => fml(x)
      case y => List(y)
    }
  }

  val nasty = List(1, List(2, List(3, List(4))), List(2, 3))

  println(fml(nasty))
  println(fml(List(1)))
  println(fml(List()))

  // problem 8 - remove consecutive dups from a list
  def noDups[A](l: List[A]): List[A] = {
    l match {
      case x :: rest => x :: noDups(rest.dropWhile(_ == x))
      case _ => Nil
    }
  }

  println(noDups(list4))
  println(noDups(List(1,2,2,3,3,3,4,4,4,4,5)))
  println(noDups(List(1)))
  println(noDups(List()))

  // problem 9 - put consecutive dups into sublists
  def clique[A](l: List[A]): List[List[A]] = {
    l match {
      case x :: rest => List(l.takeWhile(_ == x)) ::: clique(l.dropWhile(_ == x))
      case _ => Nil
    }

  }

  println(clique(List(1,2,2,3,3,3,4,4,4,4,5)))
  println(clique(List(1)))
  println(clique(List()))

  // problem 10/13 - run-length encode a list.  does not use soln to problem 9
  //  scala> encode(List('a, 'a, 'a, 'a, 'b, 'c, 'c, 'a, 'a, 'd, 'e, 'e, 'e, 'e))
  //  res0: List[(Int, Symbol)] = List((4,'a), (1,'b), (2,'c), (2,'a), (1,'d), (4,'e))

  def encode(l: List[Symbol]): List[(Int, Symbol)] = {
    l match {
      case x :: rest => (l.takeWhile(_ == x).length, x) :: encode(l.dropWhile(_ == x))
      case _ => Nil
    }
  }

  println("%%%%%%%%%%%%%%%%%%%%%%%%%%%% problem 10")
  println(encode(List('a, 'a, 'a, 'a, 'b, 'c, 'c, 'a, 'a, 'd, 'e, 'e, 'e, 'e)))

  // problem 12 - decode run-length-encoded list
  def decode(l: List[(Int, Symbol)]): List[Symbol] = {
    l flatMap {x => List.fill(x._1)(x._2)}
  }

  println("%%%%%%%%%%%%%%%%%%%%%%%%%%%% problem 12")
  println(decode(List((4,'a), (1,'b), (2,'c), (2,'a), (1,'d), (4,'e))))

  // problem 14 - duplicate elements of a list
  def dup[A](l: List[A]): List[A] = {
    l.flatMap(x => List.fill(2)(x))
  }

  println("%%%%%%%%%%%%%%%%%%%%%%%%%%%% problem 14")
  println(dup(List('a, 'a, 'b, 'c, 'd, 'c)))

  // problem 15 - duplicate elements of a list a given # of times
  def dupN[A](l: List[A], n: Int): List[A] = {
    l.flatMap(x => List.fill(n)(x))
  }

  println("%%%%%%%%%%%%%%%%%%%%%%%%%%%% problem 15")
  println(dupN(List('a, 'a, 'b, 'c, 'd, 'c), 3))

  // problem 16 - drop every nth element from a list
  def dropNth[A](l: List[A], n: Int): List[A] = {
    l match {
      case Nil => Nil
      case x: List[A] => {
        val front = if (x.length < n) x.take(n) else x.take(n).init
        front ::: dropNth(x.drop(n), n)
      }
    }
  }

  println("%%%%%%%%%%%%%%%%%%%%%%%%%%%% problem 16")
  println(dropNth(List('a, 'b, 'EEK, 'c, 'd, 'EEK, 'e, 'f), 3))

  println("%%%%%%%%%%%%%%%%%%%%%%%%%%%% problem 18")
  // problem 18 - extract slice from list.
  def slice[A](from: Int, to: Int, l: List[A]): List[A] = {
    l.drop(from).take(to - from)
  }

  println(slice(3, 7, List('a, 'b, 'c, 'd, 'e, 'f, 'g, 'h, 'i, 'j, 'k)))

  println("%%%%%%%%%%%%%%%%%%%%%%%%%%%% problem 19")
  // problem 19 - rotate list
  def rotate[A](i: Int, l: List[A]): List[A] = {
    val n = {
      val k = i % l.length
      if (k < 0) k + l.length else k
    }

    // l.drop(n) ::: l.take(n)
    val lists = l.splitAt(n)
    lists._2 ::: lists._1
  }

  println(rotate(3, List('a, 'b, 'c, 'd, 'e, 'f, 'g, 'h, 'i, 'j, 'k)))
  println(rotate(-222, List('a, 'b, 'c, 'd, 'e, 'f, 'g, 'h, 'i, 'j, 'k)))

  println("%%%%%%%%%%%%%%%%%%%%%%%%%%%% problem 21")
  // problem 21 - insert an element into a list at given position.
  def insertAt[A](insertMe: A, pos: Int, l: List[A]): List[A] = {
    l.splitAt(pos) match {
      case (front, back) => front ::: insertMe :: back
    }
  }

  println(insertAt('new, 1, List('a, 'b, 'c, 'd)))
  println(insertAt('new, 0, List('a, 'b, 'c, 'd)))
  println(insertAt('new, 4, List('a, 'b, 'c, 'd)))
  println(insertAt('new, 12, List('a, 'b, 'c, 'd)))

  println("%%%%%%%%%%%%%%%%%%%%%%%%%%%% problem 22 - list of ints in a range")

  def range(a: Int, b: Int): List[Int] = {
    (a to b).toList
  }

  println(range(4, 9))

  println("%%%%%%%%%%%%%%%%%%%%%%%%%%%% problem 26 - generate all subsets of size N")
  def combinations[A](n: Int, l: List[A]): List[List[A]] = {
    if (n > l.length) List[List[A]]()
    else if (n == 0 || l.length == 0) List(List[A]())
    else {
      val part1 = combinations(n - 1, l.tail).map(x => l.head :: x)
      val part2 = combinations(n, l.tail)
      part1 ++ part2
    }
  }

  print(combinations(3, List('a, 'b, 'c, 'd, 'e, 'f)))

//  println("%%%%%%%%%%%%%%%%%%%%%%%%%%%% problem 24")
//  println("%%%%%%%%%%%%%%%%%%%%%%%%%%%% problem 25")
//  println("%%%%%%%%%%%%%%%%%%%%%%%%%%%% problem 26")
//  println("%%%%%%%%%%%%%%%%%%%%%%%%%%%% problem 27")
//  println("%%%%%%%%%%%%%%%%%%%%%%%%%%%% problem 28")
//  println("%%%%%%%%%%%%%%%%%%%%%%%%%%%% problem 29")
//  println("%%%%%%%%%%%%%%%%%%%%%%%%%%%% problem 30")
//  println("%%%%%%%%%%%%%%%%%%%%%%%%%%%% problem 31")

}
