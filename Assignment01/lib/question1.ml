(*
 * File:   question1.ml
 * Author: Adam Edwards (with help from ChatGPT)
 * Date: 8/23/2026
 * Purpose:
 * Implement Peano arithmetic operations using recursive OCaml functions.
 * Includes multiplication and division of natural numbers represented
 * using the Peano number system.
 *)

type nat = Z | S of nat

let rec to_int n = match n with Z -> 0 | S n_prev -> 1 + to_int n_prev
let rec add x y = match x with Z -> y | S x_prev -> S (add x_prev y)
let test_add = to_int (add (S (S Z)) (S (S (S Z))))
let rec mult x y = match x with Z -> Z | S x_prev -> add y (mult x_prev y)
let test_mult = to_int (mult (S (S (S Z))) (S (S (S (S Z)))))

let rec sub x y =
  match (x, y) with
  | Z, _ -> Z
  | x, Z -> x
  | S x_prev, S y_prev -> sub x_prev y_prev

let test_sub = to_int (sub (S (S (S (S (S Z))))) (S (S Z)))

let rec less_than x y =
  match (x, y) with
  | Z, Z -> false
  | Z, S _ -> true
  | S _, Z -> false
  | S x_prev, S y_prev -> less_than x_prev y_prev

let test_less_true = less_than (S (S (S Z))) (S (S (S (S (S Z)))))
let test_less_false = less_than (S (S (S (S (S Z))))) (S (S (S Z)))

let rec div x y =
  match y with
  | Z -> failwith "division by zero"
  | _ -> if less_than x y then Z else S (div (sub x y) y)

let test_div =
  to_int
    (div (S (S (S (S (S (S (S (S (S (S (S (S Z)))))))))))) (S (S (S (S Z)))))
