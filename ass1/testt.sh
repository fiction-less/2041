
grep -E "a" ./pim
t=$(grep -E "a" ./pim | grep -Eo "5.*")

echo "$t"