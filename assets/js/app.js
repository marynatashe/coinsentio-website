
const data={tw:{tagline:'幣感 · 感知加密世界',search:'搜尋新聞、幣種、話題…',nav:['首頁','最新新聞','比特幣','以太坊','市場分析','監管政策','區塊鏈技術','Web3','DeFi'],heroLabel:'COINSENTIO · 編輯策劃',heroTitle:'讀懂加密市場的每一次脈動。',heroDesc:'全球加密貨幣、政策監管、區塊鏈技術與市場洞察，從重要訊號看見大趨勢。',focus:'政策焦點',analysis:'市場分析',heroSide1:'全球數位資產監管：新聞平台應追蹤甚麼？',heroSide2:'以太坊與區塊鏈生態：關鍵觀察方向',latest:'最新專題',market:'熱門幣種',topics:'熱門話題',footer:'幣感 — 全球加密貨幣新聞平台',disclaimer:'行情資料由 CoinGecko 提供，價格可能延遲，僅供參考，並非投資建議。網站文章目前為示範專題，並非即時新聞。',pending:'行情待接入',all:'全部',sample:'示範專題 · 非即時新聞',empty:'未找到符合條件的文章',modal:'這是一篇用於展示網站版面、文章閱讀及語言切換功能的示範內容。正式上線後，將由編輯後台發布經過來源核對的新聞，並顯示作者、發布日期及來源連結。',cats:['比特幣','以太坊','監管政策','DeFi','市場安全','新手學院'],titles:['比特幣市場：如何解讀宏觀經濟與價格波動','以太坊擴容與 Layer 2 生態的發展方向','全球加密貨幣監管政策的觀察重點','DeFi 與現實世界資產代幣化的機會與風險','保護數位資產：交易所與錢包安全基礎','從零開始理解區塊鏈與虛擬貨幣'],descs:['利率、資金流動與市場預期是重要觀察因素。','認識擴容方案及鏈上應用的技術演進。','比較不同司法管轄區的政策框架。','了解鏈上金融應用與資產代幣化。','認識私鑰、詐騙及資產保護方法。','了解數位資產的基本概念與風險。'],topicsList:['比特幣減半','全球監管政策','以太坊升級','現貨 ETF','穩定幣','AI 與區塊鏈','DeFi 生態','Web3 應用']},cn:{tagline:'币感 · 感知加密世界',search:'搜索新闻、币种、话题…',nav:['首页','最新新闻','比特币','以太坊','市场分析','监管政策','区块链技术','Web3','DeFi'],heroLabel:'COINSENTIO · 编辑策划',heroTitle:'读懂加密市场的每一次脉动。',heroDesc:'全球加密货币、监管政策、区块链技术与市场洞察，从重要信号看见大趋势。',focus:'政策焦点',analysis:'市场分析',heroSide1:'全球数字资产监管：新闻平台应追踪什么？',heroSide2:'以太坊与区块链生态：关键观察方向',latest:'最新专题',market:'热门币种',topics:'热门话题',footer:'币感 — 全球加密货币新闻平台',disclaimer:'行情数据由 CoinGecko 提供，价格可能延迟，仅供参考，并非投资建议。网站文章目前为示范专题，并非实时新闻。',pending:'行情待接入',all:'全部',sample:'示范专题 · 非实时新闻',empty:'未找到符合条件的文章',modal:'这是一篇用于展示网站版面、文章阅读及语言切换功能的示范内容。正式上线后，将由编辑后台发布经过来源核对的新闻，并显示作者、发布日期及来源链接。',cats:['比特币','以太坊','监管政策','DeFi','市场安全','新手学院'],titles:['比特币市场：如何解读宏观经济与价格波动','以太坊扩容与 Layer 2 生态的发展方向','全球加密货币监管政策的观察重点','DeFi 与现实世界资产代币化的机会与风险','保护数字资产：交易所与钱包安全基础','从零开始理解区块链与虚拟货币'],descs:['利率、资金流动与市场预期是重要观察因素。','认识扩容方案及链上应用的技术演进。','比较不同司法管辖区的政策框架。','了解链上金融应用与资产代币化。','认识私钥、诈骗及资产保护方法。','了解数字资产的基本概念与风险。'],topicsList:['比特币减半','全球监管政策','以太坊升级','现货 ETF','稳定币','AI 与区块链','DeFi 生态','Web3 应用']}};
let lang=localStorage.getItem('coinSentioLang')==='cn'?'cn':'tw',filter=-1,term='';const coins=['BTC','ETH','SOL','BNB','XRP','DOGE'];function setLang(l){lang=l;localStorage.setItem('coinSentioLang',l);document.documentElement.lang=l==='tw'?'zh-Hant':'zh-Hans';document.getElementById('tw').classList.toggle('active',l==='tw');document.getElementById('cn').classList.toggle('active',l==='cn');document.querySelectorAll('[data-t]').forEach(e=>e.textContent=data[l][e.dataset.t]);document.querySelector('[data-placeholder]').placeholder=data[l].search;render();}function render(){const d=data[lang];document.getElementById('nav').innerHTML=d.nav.map((v,i)=>`<button class="${i===0?'active':''}" onclick="navClick(${i})">${v}</button>`).join('');renderPrices();document.getElementById('topicsList').innerHTML=d.topicsList.map((x,i)=>`<div class="topic"><i>${i+1}</i>${x}</div>`).join('');document.getElementById('filters').innerHTML=[d.all,...d.cats].map((x,i)=>`<button class="${filter===i-1?'active':''}" onclick="selectFilter(${i-1})">${x}</button>`).join('');let indices=[0,1,2,3,4,5].filter(i=>(filter===-1||i===filter)&&(!term||[d.titles[i],d.descs[i],d.cats[i]].join(' ').toLowerCase().includes(term)));document.getElementById('cards').innerHTML=indices.length?indices.map(i=>`<article class="card" tabindex="0" role="button" onclick="openArticle(${i})" onkeydown="if(event.key==='Enter')openArticle(${i})"><div class="art ${['','ethereum','policy','defi','security','learn'][i]}"></div><div class="cardbody"><span class="eyebrow">${d.cats[i]}</span><h3>${d.titles[i]}</h3><p>${d.descs[i]}</p><div class="meta">${d.sample}</div></div></article>`).join(''):`<div class="empty">${d.empty}</div>`;}function selectFilter(i){filter=i;render();document.getElementById('news').scrollIntoView({behavior:'smooth'})}function navClick(i){if(i===0){filter=-1;term='';document.getElementById('query').value='';render();window.scrollTo({top:0,behavior:'smooth'});return}if(i===2)filter=0;else if(i===3)filter=1;else if(i===5)filter=2;else if(i===8)filter=3;else filter=-1;render();document.getElementById('news').scrollIntoView({behavior:'smooth'})}document.getElementById('searchForm').addEventListener('submit',e=>{e.preventDefault();term=document.getElementById('query').value.trim().toLowerCase();filter=-1;render();document.getElementById('news').scrollIntoView({behavior:'smooth'})});function openArticle(i){const d=data[lang];document.getElementById('modalCategory').textContent=d.cats[i];document.getElementById('modalTitle').textContent=d.titles[i];document.getElementById('modalMeta').textContent=d.sample;document.getElementById('modalText').textContent=d.descs[i]+' '+d.modal;document.getElementById('overlay').classList.add('open')}function closeArticle(){document.getElementById('overlay').classList.remove('open')}document.addEventListener('keydown',e=>{if(e.key==='Escape')closeArticle()});setLang(lang);

/* CoinSentio 市場價格模組 */

const coinIds = {
  BTC: 'bitcoin',
  ETH: 'ethereum',
  SOL: 'solana',
  BNB: 'binancecoin',
  XRP: 'ripple',
  DOGE: 'dogecoin'
};

let livePrices = {};
let lastPriceUpdate = null;
let priceError = false;

const priceApi =
  'https://api.coingecko.com/api/v3/simple/price' +
  '?ids=' + Object.values(coinIds).join(',') +
  '&vs_currencies=usd' +
  '&include_24hr_change=true' +
  '&include_last_updated_at=true';

function priceFormat(value) {
  if (!Number.isFinite(value)) return '—';

  const decimals = value < 1 ? 5 : 2;

  return '$' + value.toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: decimals
  });
}

function changeFormat(value) {
  if (!Number.isFinite(value)) return '—';

  return (value > 0 ? '+' : '') +
    value.toFixed(2) + '%';
}

function renderPrices() {
  const ticker = document.getElementById('ticker');
  const market = document.getElementById('marketRows');

  const pending = data[lang].pending;

  function coinHTML(symbol, compact) {
    const item = livePrices[symbol];
    const valid = item && Number.isFinite(item.usd);

    const price = valid
      ? priceFormat(item.usd)
      : 'USD —';

    const change = valid
      ? changeFormat(item.usd_24h_change)
      : pending;

    const movement = valid &&
      Number.isFinite(item.usd_24h_change)
      ? item.usd_24h_change
      : 0;

    const color = movement > 0
      ? '#21804A'
      : movement < 0
        ? '#C44B42'
        : '#777777';

    if (compact) {
      return `<div class="pill">
        <strong>${symbol}</strong>
        · ${price}
        <small style="color:${color}">
          ${change}
        </small>
      </div>`;
    }

    return `<div class="marketrow">
      <div>
        <b>${symbol}</b><br>
        <small>${price} USD</small>
      </div>
      <span style="color:${color};font-weight:700">
        ${change}
      </span>
    </div>`;
  }

  if (ticker) {
    ticker.innerHTML = coins.slice(0, 5)
      .map(symbol => coinHTML(symbol, true))
      .join('');
  }

  if (market) {
    market.innerHTML = coins
      .map(symbol => coinHTML(symbol, false))
      .join('');

    let status = document.getElementById('priceStatus');

    if (!status) {
      status = document.createElement('div');
      status.id = 'priceStatus';
      status.style.cssText =
        'font-size:12px;color:#777;margin-top:12px;';
      market.after(status);
    }

    const time = lastPriceUpdate
      ? lastPriceUpdate.toLocaleTimeString(
          lang === 'tw' ? 'zh-HK' : 'zh-CN',
          {hour: '2-digit', minute: '2-digit', second: '2-digit'}
        )
      : null;

    status.textContent = priceError
      ? (lang === 'tw'
          ? '行情更新暫時失敗'
          : '行情更新暂时失败') +
        (time ? ' · ' + time : '')
      : time
        ? (lang === 'tw'
            ? '行情更新：'
            : '行情更新：') + time
        : pending;
  }
}

async function updatePrices() {
  if (document.hidden) return;

  try {
    const response = await fetch(priceApi, {
      cache: 'no-store'
    });

    if (!response.ok) {
      throw new Error('HTTP ' + response.status);
    }

    const result = await response.json();
    const updated = {};

    for (const [symbol, id] of Object.entries(coinIds)) {
      const item = result[id];

      if (item && Number.isFinite(item.usd)) {
        updated[symbol] = item;
      }
    }

    if (!Object.keys(updated).length) {
      throw new Error('No valid prices');
    }

    livePrices = {...livePrices, ...updated};
    lastPriceUpdate = new Date();
    priceError = false;

  } catch (error) {
    console.warn('CoinSentio price update failed:', error);
    priceError = true;
  }

  renderPrices();
}

updatePrices();

setInterval(updatePrices, 60000);

document.addEventListener('visibilitychange', () => {
  if (!document.hidden) updatePrices();
});

