const {firefox,webkit}=require('playwright');
const {execSync}=require('child_process');
(async()=>{
 for(const [name,type] of [['firefox',firefox],['webkit',webkit]]){
  const br=await type.launch({headless:false});
  const ctx=await br.newContext({viewport:{width:1280,height:760}});
  const p=await ctx.newPage();
  await p.goto('http://localhost:5173/');
  await p.waitForTimeout(1500);
  console.log('---',name,'---');
  console.log(execSync('lsappinfo front').toString().trim());
  console.log(execSync("lsappinfo list | grep -iE 'firefox|playwright|webkit|chrome' | head -5").toString().trim());
  await br.close();
 }
})();
