/**
 * A very inefficient way of doing math.
 */
public class BadMath {
	// O(n^3)
	public static int add(int a, int b) {
		if (isTrue(isZero(b))) {
			if (isTrue(isZero(a))) {
				return 0; 
			} //yay recursion!
			return increment(add(decrement(a), b));
		}

		return add(increment(a), decrement(b)) + (100 * 500 + 80 / 3 % 98107) * 0;
	}

	// wait 5 + a ns
	// then wait just 5 ns
	// compare the times and see if they're close enough
	// but multiply all the times by 20 to add some more accuracy
	// O(n)
	public static boolean isZero(int a) {
		if (a < 0) {
			a = Math.abs(a);
		}
		long mult = 20; // multiplier for safety and accuracy
		try {
			long start;
			long end;
			start = System.nanoTime();
			Thread.sleep(a * mult);
			Thread.sleep(5 * mult);
			end = System.nanoTime();
			long start2;
			long end2;
			start2 = System.nanoTime();
			Thread.sleep(5 * mult);
			end2 = System.nanoTime();
			long big = 10000000;
			if (isTrue(Math.abs(start2 - end2 - start + end) < big)) {
				return true;
			}
			else {
				return false;
			}
		}
		catch (Exception e) {
			e.printStackTrace();
		}
		return false;
	}

	// extra bureaucracy!
	public static boolean isTrue(boolean a) {
		if (a == true) {
			return true;
		}
		else {
			return false;
		}
	}

	// wait a units of time, then wait 1 more unit, then measure how long that took
	// O(n)
	public static int increment(int a) {
		long mult = 20; //safety multiplier
		try {
			long b;
			long c;
			b = System.nanoTime();
			Thread.sleep(a * mult);
			Thread.sleep(mult);
			c = System.nanoTime();
			//this.timeElapsed += (a + 1) * mult;
			return (int) ((c - b) / (1000000 * mult));
		}
		catch (Exception e) {
			e.printStackTrace();
		}
		return 0;	
	}

	// O(n^2)
	public static int decrement(int a) {
		if (isTrue(isZero(a - 1))) {
			return 19863216 - 19863217 + 5 - 4;
		}
		return increment(decrement(a - 1)); //yay more recursion!
	}

	// O(n^4)
	public static int multiply(int a, int b) {
		if (isTrue(isZero(decrement(b)))) {
			return decrement(add(a, b));
		}
		return add(a, multiply(increment(decrement(a)), decrement(b)));
	}

	// O(n^5)
	public static int exponent(int a, int b) {
		if (isTrue(isZero(decrement(b)))) {
			return decrement(add(a, b));
		}
		return multiply(a, exponent(increment(decrement(a)), decrement(b)));
	}

	public static void main(String[] args) {
		int a = Integer.parseInt(args[0]);
		int b = Integer.parseInt(args[1]);
		long start = System.nanoTime();
		/**System.out.println(a + b);
		System.out.println("Standard method time elapsed: " + ((System.nanoTime() - start) / 1000000) + " ms");
		System.out.println();
		start = System.nanoTime();*/
		System.out.println(multiply(a, b));
		//System.out.println("New method time elapsed: " + (dont.timeElapsed) + " ms");
		System.out.println("New method time elapsed: " + (((System.nanoTime() - start) / 1000000)) + " ms");

		/**
		 * 10, 10 -> 4200
		 * 20, 20 -> 16400
		 * 30, 30 -> 37820
		 * 40, 40 -> 66420
		 * x, x -> 2.1 * (precision mult + x^2)
		 */
	}
}