setwd(dirname('labs/lab-05.qmd'))
# include: false
# autorun: true
library(dplyr)
covid <- read.csv("data/covid_testing.csv") |> as_tibble()
options(width = 70)

# grading helpers
pass <- function(msg = "Nice work!") list(correct = TRUE, message = msg)
fail <- function(msg) list(correct = FALSE, message = msg)
same_df <- function(a, b) {
  is.data.frame(a) && nrow(a) == nrow(b) && ncol(a) == ncol(b) &&
    isTRUE(all.equal(as.data.frame(a), as.data.frame(b), check.attributes = FALSE))
}
not_df <- fail("Your code should return a data frame. Start with `covid |>` and don't save the result with `<-`.")

.result <- local({ covid |>
  filter(result == "positive")
 })
res <- local({ # exercise: ex1
# check: true
if (!is.data.frame(.result)) {
  not_df
} else if (same_df(.result, filter(covid, result == "positive"))) {
  pass("Correct! 865 of the 15,524 tests were positive.")
} else if (nrow(.result) == 0) {
  fail("You got zero rows. Check spelling and capitalization: the value is \"positive\", all lowercase.")
} else {
  fail("Not quite. You should end up with only rows where `result` is \"positive\".")
}
 })
cat('ex1', res$correct, res$message, '\n')
.result <- local({ covid |>
  filter(result == "positive", age >= 18)
 })
res <- local({ # exercise: ex2
# check: true
target <- filter(covid, result == "positive", age >= 18)
if (!is.data.frame(.result)) {
  not_df
} else if (same_df(.result, target)) {
  pass("Correct! 342 positive tests came from adults.")
} else if (nrow(.result) == nrow(filter(covid, result == "positive", age > 18))) {
  fail("Close. Did you use `>` instead of `>=`? 18-year-olds count.")
} else {
  fail("Not quite. Keep rows that are positive AND have age of at least 18.")
}
 })
cat('ex2', res$correct, res$message, '\n')
.result <- local({ covid |>
  select(subject_id, age, demo_group) |>
  arrange(desc(age))
 })
res <- local({ # exercise: ex3
# check: true
if (!is.data.frame(.result)) {
  not_df
} else if (nrow(.result) == nrow(covid) && isTRUE(.result$age[1] == max(covid$age)) &&
           !is.unsorted(rev(.result$age))) {
  pass("Sorted! Now look at the top rows. Do those ages look believable?")
} else if (isTRUE(.result$age[1] == min(covid$age))) {
  fail("That's youngest to oldest. Use `desc(age)` to flip the order.")
} else {
  fail("Not quite. Sort by `age`, largest first.")
}
 })
cat('ex3', res$correct, res$message, '\n')
.result <- local({ covid |>
  select(subject_id, age, clinic_name, result)
 })
res <- local({ # exercise: ex4
# check: true
want <- c("subject_id", "age", "clinic_name", "result")
if (!is.data.frame(.result)) {
  not_df
} else if (identical(names(.result), want)) {
  pass()
} else if (setequal(names(.result), want)) {
  fail("Right columns, wrong order. List them in the order asked.")
} else {
  fail(paste0("Your columns are: ", paste(names(.result), collapse = ", "),
              ". You need: ", paste(want, collapse = ", "), "."))
}
 })
cat('ex4', res$correct, res$message, '\n')
.result <- local({ covid |>
  mutate(age_months = age * 12) |>
  select(subject_id, age, age_months)
 })
res <- local({ # exercise: ex5
# check: true
if (!is.data.frame(.result)) {
  not_df
} else if (!"age_months" %in% names(.result)) {
  fail("I can't find a column called `age_months`. Check the spelling on the left of `=`.")
} else if (isTRUE(all.equal(.result$age_months, covid$age * 12))) {
  pass()
} else {
  fail("`age_months` has the wrong values. Multiply `age` by 12.")
}
 })
cat('ex5', res$correct, res$message, '\n')
.result <- local({ covid |>
  count(clinic_name, sort = TRUE)
 })
res <- local({ # exercise: ex6
# check: true
target <- count(covid, clinic_name, sort = TRUE)
if (!is.data.frame(.result)) {
  not_df
} else if (same_df(.result, target)) {
  pass("Correct! The clinical lab collected the most tests (7,500).")
} else if (same_df(arrange(.result, clinic_name), arrange(target, clinic_name))) {
  fail("Right counts, but sort them so the biggest is at the top.")
} else {
  fail("Not quite. Count by `clinic_name` and sort.")
}
 })
cat('ex6', res$correct, res$message, '\n')
.result <- local({ covid |>
  group_by(drive_thru_ind) |>
  summarize(
    n = n(),
    pct_positive = mean(result == "positive") * 100
  )
 })
res <- local({ # exercise: ex7
# check: true
target <- covid |> group_by(drive_thru_ind) |>
  summarize(n = n(), pct_positive = mean(result == "positive") * 100)
if (!is.data.frame(.result)) {
  not_df
} else if (same_df(.result, target)) {
  pass("Correct! About 6.0% positive at the drive-through vs. 5.1% elsewhere.")
} else if (nrow(.result) == 1) {
  fail("Only one row came back, so nothing was grouped. Fill in `group_by()`.")
} else {
  fail("Not quite. Group by `drive_thru_ind`.")
}
 })
cat('ex7', res$correct, res$message, '\n')
.result <- local({ covid |>
  group_by(demo_group) |>
  summarize(median_age = median(age))
 })
res <- local({ # exercise: ex8
# check: true
target <- covid |> group_by(demo_group) |> summarize(median_age = median(age))
if (!is.data.frame(.result)) {
  not_df
} else if (same_df(.result, target)) {
  pass("Correct! Patients have a median age of 5. This is a children's hospital.")
} else if (!"median_age" %in% names(.result)) {
  fail("Name your summary column `median_age`.")
} else {
  fail("Not quite. Group by `demo_group`, then summarize `median(age)`.")
}
 })
cat('ex8', res$correct, res$message, '\n')
.result <- local({ covid |>
  filter(demo_group == "patient", result != "invalid") |>
  group_by(gender) |>
  summarize(
    n = n(),
    pct_positive = round(mean(result == "positive") * 100, 1)
  )
 })
res <- local({ # exercise: ex9
# check: true
target <- covid |>
  filter(demo_group == "patient", result != "invalid") |>
  group_by(gender) |>
  summarize(n = n(), pct_positive = round(mean(result == "positive") * 100, 1))
if (!is.data.frame(.result)) {
  not_df
} else if (same_df(.result, target)) {
  pass("Excellent! 4.9% of tests for female patients and 4.2% for male patients were positive.")
} else if (nrow(.result) == 2 && isTRUE(sum(.result$n) != sum(target$n))) {
  fail("You have the right groups but the wrong number of tests. Check both `filter()` conditions.")
} else {
  fail("Not quite. Filter, then group by `gender`, then summarize.")
}
 })
cat('ex9', res$correct, res$message, '\n')