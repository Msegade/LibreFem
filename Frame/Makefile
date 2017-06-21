.PHONY: all

TARGET=frame
MESHFORMAT=med

solve: $(TARGET).resu

$(TARGET).resu: $(TARGET).export $(TARGET).comm $(TARGET).$(MESHFORMAT)
	tmpfile=$<.tmp
	cp $< "$tmpfile"
	as_run "$tmpfile"
	rm "$tmpfile"

clean:
	rm -rf $(TARGET).{rmed,base,resu,mess}
	rm -rf mpfile
