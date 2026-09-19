const fs = require("fs");
const path = require("path");

const outputDir = path.join(__dirname, "signatures");

if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}
const employees = [
  { name: "Althia Kapp", position: "Senior Account Manager", phone: "044 382 0565", email: "althia@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/althia-3-400x400-circle-v1.png" },
  { name: "Annemarie Luck", position: "Head of Strategy", phone: "084 999 5257", email: "annemarie@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa/annemarie-luck-400x400transparent.png" },
  { name: "Ashleigh van Loggerenberg", position: "Junior Copywriter", phone: "064 365 4467", email: "Ashleigh@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/ashleigh-3-400x400-circle-v1.png" },

  { name: "Anthony Lightening", position: "Digital Marketing Intern", phone: "044 382 0565", email: "anthony@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/anthony-4-400x400-circle-v1.png" },
  { name: "Monique Myburgh", position: "Growth Marketer", phone: "044 382 0565", email: "monique@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/monique-3-400x400-circle-v1.png" },
  { name: "Anri van Der Linde", position: "Growth Marketer", phone: "044 382 0565", email: "anri@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/anri-2-400x400-circle-v1.png" },
  { name: "Aimee Henley", position: "Office Administration & PA", phone: "044 382 0565", email: "aimee@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/aimee-3-400x400-circle-v1.png" },

  { name: "Candice Masson", position: "Director of Growth", phone: "078 544 7782", email: "candice@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/candice-2-400x400-circle-v1.png" },
  { name: "Carla Engelbrecht", position: "Junior Designer", phone: "084 729 3414", email: "carla@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/carla-4-400x400-circle-v1.png" },
  
  { name: "Elizna Steyn", position: "Account Manager", phone: "083 950 5998", email: "Elizna@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/elizna-4-400x400-circle-v1.png" },
  { name: "Elran Meiring", position: "Director of Paid Media", phone: "071 494 5189", email: "Elran@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa/elran-meiring-400x400transparent.png" },
  { name: "Etienne Bruwer", position: "Founding Partner & CEO", phone: "082 305 8213", email: "etienne@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa/etienne-bruwer-400x400transparent.png" },
  { name: "Eugene Bredenkamp", position: "Studio Director", phone: "079 060 7844", email: "eugene@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/eugene-4-400x400-circle-v1.png" },
  { name: "Fergus David Hannah", position: "Videographer/Editor", phone: "082 411 3920", email: "fergus@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa/fergus-david-hannah-400x400transparent.png" },
  { name: "Gabrielle Zondagh", position: "Account Coordinator", phone: "072 225 4850", email: "Gabrielle@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa/gabrielle-zondagh-400x400transparent.png" },
  { name: "Gemma Persello", position: "Senior Social Media Strategist", phone: "078 774 8835", email: "gemma@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/gemma-2-400x400-circle-v1.png" },
  { name: "Gerrie van Niekerk", position: "Junior Partner & CFO", phone: "084 200 0823", email: "gerrie@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/gerrie-4-400x400-circle-v1.png" },
  { name: "Greg Hall", position: "SEO/PPC Specialist", phone: "082 798 2660", email: "greg@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa/greg-hall-400x400transparent.png" },
  { name: "Gigh Zack", position: "Animation Lead", phone: "078 686 9971", email: "Guy@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/gigh-4-400x400-circle-v1.png" },
  { name: "Jean-Paul Brouard", position: "Designer", phone: "083 997 7987", email: "jp@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa/jean-paul-brouard-400x400transparent.png" },
  { name: "Jess van der Merwe", position: "Junior Designer", phone: "066 054 6464", email: "Jess@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/jess-4-400x400-circle-v1.png" },
  { name: "Jomarie Voges", position: "Financial Controller", phone: "082 269 7542", email: "jomarie@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/jomarie-6-400x400-circle-v1.png" },
  { name: "Kayla Spinelli", position: "Office Administration/PA", phone: "081 476 6721", email: "Kayla@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa/kayla-spinelli-400x400transparent.png" },
  { name: "Kendel Falkson", position: "PR Agent", phone: "082 905 2656", email: "Kendel@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa/kendel-falkson-400x400transparent.png" },
  { name: "Lani Bruwer", position: "Web Developer & Information Architect", phone: "084 452 2304", email: "lani@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa/lani-bruwer-400x400transparent.png" },
  { name: "LeeAnn Visser", position: "Video Producer", phone: "078 675 6476", email: "lee@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/lee-3-400x400-circle-v1.png" },
  { name: "Marie Hentschel", position: "Senior Account Manager", phone: "076 943 5538", email: "marie@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/marie-4-400x400-circle-v1.png" },
  { name: "Micaela Cox", position: "Motion Graphics Designer", phone: "082 977 5880", email: "Micaela@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa/micaela-cox-400x400transparent.png" },
  { name: "Mihlali Vumazonke", position: "Social Media Manager", phone: "067 252 7987", email: "Mihlali@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/mihlali-2-400x400-circle-v1.png" },
  { name: "Nicelle Bresler", position: "Senior Copywriter & Strategist", phone: "082 295 1396", email: "Nicell@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa/nicelle-bresler-400x400transparent.png" },
  { name: "Noël Scholtz", position: "Director of Video", phone: "072 070 5996", email: "noel@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/noel-2-400x400-circle-v1.png" },
  { name: "Nuhaa Davis", position: "Copywriter", phone: "079 467 4386", email: "Nuhaa@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/nuhaa-4-400x400-circle-v1.png" },
  { name: "Portia Matha", position: "Junior Web Developer", phone: "064 999 3847", email: "portia@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/portia-2-400x400-circle-v1.png" },
  { name: "Riana Wiechers", position: "Copywriter", phone: "063 687 4517", email: "riana@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa/riana-wiechers-400x400transparent.png" },
  { name: "Riëtte Bester", position: "Copywriter", phone: "082 058 3483", email: "riette@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/riette-4-400x400-circle-v1.png" },
  { name: "Simeon Bezuidenhout", position: "Head of Video", phone: "071 462 0366", email: "simeon@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/simeon-2-400x400-circle-v1.png" },
  { name: "Tshituku Ndadza", position: "Social Media Manager", phone: "078 593 5815", email: "Tshituku@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/tshituku-2-400x400-circle-v1.png" },
  { name: "Willem van der Merwe", position: "Content Creator", phone: "082 799 5884", email: "Willem@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa-2025/willem-4-400x400-circle-v1.png" },
  { name: "Greg Hall", position: "SEO/PPC Specialist", phone: "082 798 2660", email: "greg@mag.cr", image: "https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/headshots/sa/greg-hall-400x400transparent.png" }
];




employees.forEach(employee => {
    const fileName = `${employee.name.replace(/\s+/g, '_')}.html`;
    const filePath = path.join(outputDir, fileName);

    const htmlContent =`<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${employee.name} - Signature</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; flex-direction: column; align-items: center; }
        .steps { display: flex; flex-direction: column; gap: 30px; }
        .steps span { font-size: 20px; }
    </style>
</head>
<body>
    <div id="content">
    <table style="font-family: Arial, Helvetica, sans-serif; width: 504px; border-collapse: collapse; height: 151px;">
        <tbody>
            <tr style="height: 151px;">
                <td style="vertical-align: top; padding-top: 5px; padding-right: 5px; width: 150.297px; height: 151px;">
                    <img src="${employee.image}" alt="${employee.name}" width="150" height="149" />
                </td>
                <td style="vertical-align: top; width: 342.703px; height: 151px;">
                    <span style="font-size: 28px; color: black; font-family: 'Times New Roman', serif;">${employee.name}</span><br />
                    <span style="color: #b59756;">${employee.position}</span> 
                    <br />
                    <table style="margin-top: 10px;">
                        <tbody>
                            <tr>
                                <td style="vertical-align: middle;">
                                    <img src="https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/icons/mail.png" alt="" width="18" />
                                </td>
                                <td style="vertical-align: middle; padding-left: 5px;">
                                    <a style="text-decoration: none; border-bottom: none; color: #333333;" href="mailto:${employee.email}">${employee.email}</a>
                                </td>
                            </tr>
                            <tr>
                                <td style="vertical-align: middle;">
                                    <img src="https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/icons/globe.png" alt="" width="18" />
                                </td>
                                <td style="vertical-align: middle; padding-left: 5px;">
                                    <a style="text-decoration: none; border-bottom: none; color: #333333;" href="https://magneticcreative.com/" target="_blank">magneticcreative.com</a>
                                </td>
                            </tr>
                            <tr>
                                <td style="vertical-align: middle;">
                                    <img src="https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/icons/smartphone.png" alt="" width="18" />
                                </td>
                                <td style="vertical-align: middle; padding-left: 5px;">
                                    <a style="text-decoration: none; border-bottom: none; color: #333333;" href="tel:${employee.phone}">${employee.phone}</a>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
        </tbody>
    </table>
</div>

<br><br>
    <span>Step 1</span>
<button id="btn">Click here to copy</button>
<br><br>

<div class="steps">
    <span>Step 2: Go to <a href="https://mail.google.com/mail" target="_blank">Gmail.com</a> and click on settings</span>

    <img src="./assets/step 2.png" alt="">
    <span>Click on See all settings</span>
    <img src="./assets/step 3.png" alt="">
    <span>Scroll down and click on Create new button</span>
    <img src="./assets/step 4.png" alt="">
    <span>Add name, click on Create</span>
    <img src="./assets/step 5.png" alt="">
    <span>Paste the signature and select it on "For New emails use" and "On reply/forward use" then save changes</span>
    <img src="./assets/step 6.png" alt="">
</div>
</body>

<style>
    body{
        display: flex;
    flex-direction: column;
    align-items: center;
    }
    .steps{
        display: flex;
        flex-direction: column;
        gap: 30px;
    }
    .steps span{
        font-size: 28px;
    }
    
</style>
<script>
    document.getElementById("btn").addEventListener("click", async function() {
        const content = document.getElementById("content").outerHTML;
        
        try {
            await navigator.clipboard.write([
                new ClipboardItem({
                    "text/html": new Blob([content], { type: "text/html" })
                })
            ]);
            alert("Copied");
        } catch (err) {
            console.error("Error: ", err);
            alert("Error. Ask Gabo");
        }
    });
</script>
</body>
</html>`;

fs.writeFileSync(filePath, htmlContent);
});
