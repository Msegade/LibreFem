.PHONY: all
TARGET=springs
solve: $(TARGET).resu


$(TARGET)Study.resu: $(TARGET).export $(TARGET).comm $(TARGET).mail
	tmpfile=$<.tmp
	cp $< "$tmpfile"
	as_run "$tmpfile"
	rm "$tmpfile"

clean:
	rm -rf $(TARGET).{rmed,base,resu,mess}
	rm -rf mpfile
	rm -rf stiffness.csv
