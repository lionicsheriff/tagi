;; some sample text

(defface tagi-link-exists
  '((t(:weight bold
	       :foreground "blue")))
  "Face for link that has a file"
  :group 'tagi)

(defface tagi-link-missing
  '((t(:weight bold
	       :foreground "red")))
  "Face for link that does not have a file"
  :group 'tagi)


(defface tagi-link-mouse-highlight
  '((t(:underline t)))
  "Face for link that has a mouse over it"
  :group 'tagi)

(defun tagi/follow-link (file)
  ""
  (message (concat "following link:" file)))

(defun tagi/mouse-click-link (event)
  ""
  (interactive "e")
  (let ((file (get-char-property (posn-point (cadr event)) 'tagi-file-path)))
    (tagi/follow-link file )))

(defun tagi/set-link (start end file)
  ""
  (let ((tagi-overlay (make-overlay start end))
	(keymap (make-sparse-keymap)))`
    (overlay-put tagi-overlay 'name 'tagi-link)
    
    ;; store the file location
    (overlay-put tagi-overlay 'tagi-file-path file)
    
    ;; indicate that the text is a link
    (overlay-put tagi-overlay 
		 (if font-lock-mode 'font-lock-face 'face)
		 'tagi-link-exists)

    ;; Make the link clickable
    (overlay-put tagi-overlay 
		 'mouse-face
		 'tagi-link-mouse-highlight)
    (define-key keymap [mouse-2] 'tagi/mouse-click-link)
    (define-key keymap [follow-link] 'mouse-face)
    
    (overlay-put tagi-overlay 'keymap keymap)))

(progn 
  (remove-overlays (point-min) (point-max) 'tagi-link)
  (tagi/set-link 0 5 "/test.txt")
  (tagi/set-link 50 55 "/test2.txt"))

(get-char-property 4 'tagi-file-path)


(overlays-in 3 5)



(defun mbg/make-line-bold ()
  (interactive)
  (overlay-put
   (make-overlay
    (line-beginning-position)
    (line-end-position))
   'font-lock-face 'tagi-link-exists))

