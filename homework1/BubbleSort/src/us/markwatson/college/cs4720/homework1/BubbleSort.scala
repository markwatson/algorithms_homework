[]
ortewq
package us.markwatson.college.cs4720.homework1

import scala.util
import compat.Platform
import collection.mutable.HashMap

/**
 * Bubble Sort
 * 
 * Written for Homework 1 for CS 4720, Fall 2011
 * Mark Watson
 * 
 */

object BubbleSort {
  /**
   * Takes an array of ints and does a bubble sort on them.
   */
  def bubbleSort(a: Array[Int]) {
    var temp = 0

    for (i <- 0 until a.length) {
      for (j <- ((i+1) until a.length).reverse) {
        if (a(j) < a(j-1)) {
          // do the swap
          temp = a(j)
          a(j) = a(j-1)
          a(j-1) = temp
        }
      }
    }

    a
  }

  case class SortSequence(seq: Array[Int], var runTime: Long)

  def main(args: Array[String]) {
    // Generate a bunch of randomly ordered sequences.
    val step = 1000
    val max = 100000
    val rand = new util.Random()
    val seqs = new HashMap[Int, SortSequence]()
    for (seqLength <- 0.until(max, step)) {
      seqs.put(seqLength, new SortSequence(rand.shuffle((0 until seqLength).toList).toArray, 0))
    }

    // Run the sort on all the sequences
    Platform.collectGarbage()
    for ((l, s) <- seqs) {
      val startTime = Platform.currentTime
      bubbleSort(s.seq)
      val endTime = Platform.currentTime
      s.runTime = endTime - startTime
      Platform.collectGarbage()
    }

    // Output the results
    for ((l, s) <- seqs) {
      println(l.toString + "," + s.runTime.toString)
    }

  }
}