const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const dir = 'c:\\Users\\Public\\Projects\\Testing_HCMUS\\HW4\\eshop-sut\\submission';
const files = fs.readdirSync(dir).filter(f => f.startsWith('BUG-') && f.endsWith('.md'));

for (const file of files) {
    const fullPath = path.join(dir, file);
    const content = fs.readFileSync(fullPath, 'utf8');
    
    // Parse title
    const match = content.match(/title:\s*'(.*?)'/);
    const title = match ? match[1] : `Issue for ${file}`;
    
    // Parse body (strip frontmatter)
    const body = content.replace(/^---(?:\r?\n)[\s\S]*?---(?:\r?\n)/, '');
    
    const tempFile = path.join(require('os').tmpdir(), `temp_body_${file}`);
    fs.writeFileSync(tempFile, body, 'utf8');
    
    console.log(`Creating issue: ${title}`);
    try {
        const out = execSync(`gh issue create --title "${title.replace(/"/g, '\\"')}" --body-file "${tempFile}"`, { encoding: 'utf8' });
        console.log("Success:", out.trim());
    } catch(e) {
        console.error("Error creating issue:", e.stderr || e.message);
    }
    if(fs.existsSync(tempFile)){
        fs.unlinkSync(tempFile);
    }
}
