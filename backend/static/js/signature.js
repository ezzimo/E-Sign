async function initializeSignaturePage(email, signatureRequestId) {
	const documentLinks = document.querySelectorAll(".document-link");
	const pdfContainer = document.getElementById("pdf-container");
	const nextDocButton = document.getElementById("next-doc");
	const prevDocButton = document.getElementById("prev-doc");
	const drawSignButton = document.getElementById("draw-signature-btn");
	const signButton = document.getElementById("sign-btn");
	const emailInput = document.getElementById("otp-email-input");
	const otpInput = document.getElementById("otp-input");
	const sendOtpBtn = document.getElementById("send-otp-btn");
	const verifyOtpBtn = document.getElementById("verify-otp-btn");
	let currentDocIndex = 0;
	const viewedDocs = new Map();

	// Initialize the first document display
	updateDocumentDisplay(currentDocIndex);

	documentLinks.forEach((link, index) => {
		viewedDocs.set(index, false);
		link.addEventListener("click", (event) => {
			event.preventDefault();
			updateDocumentDisplay(index);
		});
	});

	async function updateDocumentDisplay(index) {
		const urls = JSON.parse(
			documentLinks[index].dataset.urls.replace(/'/g, '"'),
		);
		currentDocIndex = index;
		console.log("Loading images for document index:", index, "URLs:", urls);
		await loadImages(urls);
		attachScrollListener(index);
		updateButtonStates();
	}

	async function loadImages(urls) {
		pdfContainer.innerHTML = "";
		for (const url of urls) {
			const img = document.createElement("img");
			img.src = url;
			img.style.width = "100%";
			img.onload = () => console.log("Loaded image:", url);
			img.onerror = (err) => console.error("Error loading image:", url, err);
			pdfContainer.appendChild(img);
		}
	}

	function attachScrollListener(index) {
		console.log(`Attaching scroll listener to document ${index}`);
		pdfContainer.addEventListener("scroll", () => checkScrollToEnd(index), {
			passive: true,
		});
	}

	function checkScrollToEnd(index) {
		const scrollTop = pdfContainer.scrollTop;
		const scrollHeight = pdfContainer.scrollHeight;
		const clientHeight = pdfContainer.clientHeight;
		const scrolledToEnd = scrollTop + clientHeight >= scrollHeight - 5;
		if (scrolledToEnd && !viewedDocs.get(index)) {
			console.log(`Document ${index} viewed`);
			viewedDocs.set(index, true);
			documentLinks[index].parentElement.querySelector(
				".read-status",
			).textContent = "(Read)";
			checkAllDocumentsViewed();
		}
	}

	function checkAllDocumentsViewed() {
		const allViewed = Array.from(viewedDocs.values()).every((status) => status);
		signButton.disabled = !allViewed;
		nextDocButton.disabled =
			!viewedDocs.get(currentDocIndex) ||
			currentDocIndex === documentLinks.length - 1;
	}

	function updateButtonStates() {
		prevDocButton.disabled = currentDocIndex === 0;
		nextDocButton.disabled = currentDocIndex === documentLinks.length - 1;
	}

	nextDocButton.addEventListener("click", () => {
		if (currentDocIndex < documentLinks.length - 1) {
			updateDocumentDisplay(currentDocIndex + 1);
		}
	});

	prevDocButton.addEventListener("click", () => {
		if (currentDocIndex > 0) {
			updateDocumentDisplay(currentDocIndex - 1);
		}
	});

	drawSignButton.addEventListener("click", () => {
		$("#signatureModal").modal("show");
	});

	sendOtpBtn.addEventListener("click", sendOtp);
	verifyOtpBtn.addEventListener("click", verifyOtp);

	function sendOtp() {
		sendOtpBtn.disabled = true;
		fetch("/api/v1/signe/send_otp", {
			method: "POST",
			headers: {
				"Content-Type": "application/x-www-form-urlencoded",
			},
			body: new URLSearchParams({
				email: emailInput.value,
				signature_request_id: signatureRequestId,
			}),
		})
			.then((response) => {
				sendOtpBtn.disabled = false;
				if (response.ok) {
					alert("OTP sent successfully");
					otpInput.disabled = false;
					verifyOtpBtn.disabled = false;
				} else {
					alert("Failed to send OTP");
					otpInput.disabled = true;
					verifyOtpBtn.disabled = true;
				}
			})
			.catch((error) => {
				alert("Error sending OTP: " + error.message);
				sendOtpBtn.disabled = false;
			});
	}

	function verifyOtp() {
		verifyOtpBtn.disabled = true;
		fetch("/api/v1/signe/verify_otp", {
			method: "POST",
			headers: {
				"Content-Type": "application/x-www-form-urlencoded",
			},
			body: new URLSearchParams({
				email: emailInput.value,
				otp: otpInput.value,
				signature_request_id: signatureRequestId,
			}),
		})
			.then((response) => {
				verifyOtpBtn.disabled = false;
				if (response.ok) {
					alert("Document signed successfully");
					$("#otpModal").modal("hide");
					resetModal();
					window.location.href = "/success"; // Redirect to the success page
				} else {
					alert("Failed to verify OTP");
				}
			})
			.catch((error) => {
				alert("Error verifying OTP: " + error.message);
				verifyOtpBtn.disabled = false;
			});
	}

	function resetModal() {
		otpInput.value = "";
		otpInput.disabled = true;
		verifyOtpBtn.disabled = true;
	}

	signButton.addEventListener("click", () => {
		$("#signatureModal").modal("show");
	});

	const signaturePad = document
		.getElementById("signature-canvas")
		.getContext("2d");
	const clearButton = document.getElementById("clear-signature-btn");
	const saveButton = document.getElementById("save-signature-btn");
	const signatureModal = $("#signatureModal");
	let isDrawing = false;

	document
		.getElementById("signature-canvas")
		.addEventListener("mousedown", startDrawing);
	document
		.getElementById("signature-canvas")
		.addEventListener("mousemove", draw);
	document
		.getElementById("signature-canvas")
		.addEventListener("mouseup", stopDrawing);
	document
		.getElementById("signature-canvas")
		.addEventListener("mouseleave", stopDrawing);

	clearButton.onclick = () => {
		signaturePad.clearRect(
			0,
			0,
			signaturePad.canvas.width,
			signaturePad.canvas.height,
		);
	};

	saveButton.onclick = () => {
		const signatureData = signaturePad.canvas.toDataURL("image/png");
		console.log("Signature Data:", signatureData);
		signatureModal.modal("hide");
	};

	function startDrawing(e) {
		isDrawing = true;
		signaturePad.beginPath();
		signaturePad.moveTo(e.offsetX, e.offsetY);
	}

	function draw(e) {
		if (!isDrawing) return;
		signaturePad.lineTo(e.offsetX, e.offsetY);
		signaturePad.stroke();
	}

	function stopDrawing() {
		isDrawing = false;
	}
}
