////////////////////////// chapter 1

def compose[A, B, C](g: B => C, f: A => B): A => C = (a: A) => g(f(a))


def fuse[A, B](a: Option[A], b: Option[B]): Option[(A, B)] = {
  for {
    // because of the way for comprehensions work, if a or b are
    // None, the entire expression is None.
    i <- a
    j <- b
    k <- Some(i, j)
  } yield k
}

fuse[Int, Int](None, None)
fuse[Int, Int](Some(3), Some(4))
fuse[Int, Int](None, Some(3))

def check[T](xs: Seq[T])(pred: T => Boolean): Boolean = {
  try {
    !xs.map(pred(_)).contains(false)
  }
  catch {
    case _: Exception => false
  }
}

// should return false
check[Int](0 until 10)(40 / _ > 0)

// should return true
check[Int](1 until 10)(40 / _ > 0)



//////////////////////////// chapter 2

def parallel[A, B](a: => A, b: => B): (A, B) = {

  val a_thread = new Thread {
    override def run: A = {
      var a_result: A = a
    }
  }
  ???
}