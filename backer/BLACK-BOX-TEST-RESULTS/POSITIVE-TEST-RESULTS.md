API="http://127.0.0.1:8000/ask"

cat > /tmp/abb_positive.txt <<'EOF'
Kartımı itirdim, necə bloklayım?
PIN kodu unutsam nə etməliyəm?
3D Secure necə aktiv edilir?
ABB Randevu xidməti nədir?
ABB-nin poçt ünvanı nədir?
Məlumat Mərkəzi hansı xidmətləri göstərir?
ATM-lərdə Cash-In dəstəyi varmı?
ABB mobile təhlükəsizlik sertifikatı nədir?
ABB mobile-dan nağd kredit necə alınır?
Nağd kredit kimlərə verilir?
Həftə içi filialların iş saatı neçədir?
Şənbə günü hansı filiallar işləyir?
What security certification does ABB mobile mention?
How can I block my card in ABB mobile?
Where can I find ABB branch and ATM map?
Какие контакты для обращений и жалоб указаны у ABB?
What is ABB Randevu?
EOF

pass=0
fail=0

while IFS= read -r q; do
  ans=$(curl -s -X POST "$API" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg q "$q" '{question:$q}')" | jq -r '.answer // ""')

  low=$(printf "%s" "$ans" | tr '[:upper:]' '[:lower:]')

  if echo "$low" | grep -Eq "bunu bilmirəm|bilmirəm|i don't know|i do not know|не знаю"; then
    result_flag="FAIL"
    fail=$((fail+1))
  else
    result_flag="PASS"
    pass=$((pass+1))
  fi

  printf "\n[%s]\nQ: %s\nA: %s\n" "$result_flag" "$q" "$ans"
done < /tmp/abb_positive.txt

printf "\nSummary: PASS=%d FAIL=%d TOTAL=%d\n" "$pass" "$fail" "$((pass+fail))"
