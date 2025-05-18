let userAgent = {
    icon: null,
    name: null,
    mission: null,
    file: null
  };
  
  document.querySelectorAll(".icon-card").forEach(card => {
    card.addEventListener("click", () => {
      // Remove selection from all
      document.querySelectorAll(".icon-card").forEach(c => c.classList.remove("selected"));
      // Add selection
      card.classList.add("selected");
      userAgent.icon = card.getAttribute("data-icon");
    });
  });
  
  function goToStep2() {
    if (!userAgent.icon) {
      alert("Please select an icon.");
      return;
    }
    document.getElementById("step1").classList.remove("active");
    document.getElementById("step2").classList.add("active");
  }

  function goToStep3() {
    const nameInput = document.getElementById("agentName").value.trim();
    
    if (!nameInput) {
        alert("Please enter a name for your agent.");
        return;
    }
    
    userAgent.name = nameInput;
    
    document.getElementById("step2").classList.remove("active");
    document.getElementById("step3").classList.add("active");
    }
    function goToStep4() {
        const mission = document.getElementById("agentMission").value.trim();
      
        if (!mission) {
          alert("Please describe the agent’s mission.");
          return;
        }
      
        userAgent.mission = mission;
      
        document.getElementById("step3").classList.remove("active");
        document.getElementById("step4").classList.add("active");
      }

      function goToStep5() {
        const fileInput = document.getElementById("knowledgeFile");
        const file = fileInput.files[0];
      
        if (!file) {
          alert("Please upload a knowledge file for your agent.");
          return;
        }
      
        userAgent.file = file;
      
        document.getElementById("step4").classList.remove("active");
        document.getElementById("step5").classList.add("active");
      
        // Show agent summary
        document.getElementById("agentSummary").innerHTML = `
          <p><strong>Icon:</strong> ${userAgent.icon}</p>
          <p><strong>Name:</strong> ${userAgent.name}</p>
          <p><strong>Mission:</strong> ${userAgent.mission}</p>
          <p><strong>File:</strong> ${userAgent.file.name}</p>
        `;
      }

      async function submitAgent() {
        const formData = new FormData();
        formData.append("file", userAgent.file);
        formData.append("usecase", `${userAgent.name} - ${userAgent.mission}`);
      
        const res = await fetch("http://127.0.0.1:8000/upload", {
          method: "POST",
          body: formData,
        });
      
        const data = await res.json();
      
        // 🧠 Read the file content and store it in userAgent.knowledgeText
        const reader = new FileReader();
        reader.onload = function () {
          userAgent.knowledgeText = reader.result;
        };
        reader.readAsText(userAgent.file);
      
        // ⛱️ Move to the chat screen
        document.getElementById("step5").classList.remove("active");
        document.getElementById("chatScreen").classList.add("active");
      
        document.getElementById("agentAvatar").src = `../icons/${userAgent.icon}`;
        document.getElementById("agentDisplayName").innerText = userAgent.name;
        document.getElementById("agentMissionInfo").innerText = userAgent.mission;
        document.getElementById("agentFilesInfo").innerText = userAgent.file.name;
      
        appendMessage("agent", data.bot_response);
      }
      function toggleAgentInfo() {
        const infoBox = document.getElementById("agentInfo");
        infoBox.style.display = infoBox.style.display === "none" ? "block" : "none";
      }
      
      function appendMessage(sender, text) {
        const chatBox = document.getElementById("chatBox");
        const msg = document.createElement("div");
        msg.style.margin = "0.5rem 0";
        msg.style.textAlign = sender === "user" ? "right" : "left";
        msg.innerHTML = `<strong>${sender === "user" ? "You" : userAgent.name}:</strong> ${text}`;
        chatBox.appendChild(msg);
        chatBox.scrollTop = chatBox.scrollHeight;
      }
      
      async function sendMessage() {
        const input = document.getElementById("userInput");
        const userText = input.value.trim();
        if (!userText) return;
      
        appendMessage("user", userText);
        input.value = "";
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              message: userText,
              icon: userAgent.icon,
              name: userAgent.name,
              mission: userAgent.mission,
              knowledge: userAgent.knowledgeText
            })
          });
      
        const data = await response.json();
        appendMessage("agent", data.response);
      }