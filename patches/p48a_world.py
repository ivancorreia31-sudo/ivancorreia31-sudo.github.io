# build 48 (a): the day's event fits the weather and the season - no heatwave on a rainy day or in winter - with a
# cold snap for winter, and rain that's likelier in autumn and winter than in summer
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("""  potholes: ['m_kerbed', 'm_bangspring',""",
    """  coldsnap: ['flatbatt', 'winter', 'nostart', 'clicks', 'coldheater', 'starting', 'charging', 'dimlights', 'washers', 'm_wipers'],
  potholes: ['m_kerbed', 'm_bangspring',""")
rep("""  { id: 'busy', title: 'Busy morning', text: 'Two extra customers are already waiting on the board.', extra: 2 },
];""", """  { id: 'busy', title: 'Busy morning', text: 'Two extra customers are already waiting on the board.', extra: 2 },
  { id: 'coldsnap', title: 'Cold snap', text: 'A hard frost overnight. Flat batteries, non-starters and cold heaters pay 50% more labour.', match: c => EV_TAGS.coldsnap.includes(c.id), labour: 1.5 },
];
/* build 48: an event has to suit the day - a heatwave only on a dry summer day, a cold snap only in winter, pothole
   season any time but summer - and it rains more in autumn and winter */
const evFits48 = e => { const se = seasonOf(S.day), wet = S.weather === 'rain';
  if (e.id === 'heatwave') return se === 'Summer' && !wet;
  if (e.id === 'coldsnap') return se === 'Winter';
  if (e.id === 'potholes') return se !== 'Summer';
  return true; };
const rain48 = d => ({ Spring: 0.22, Summer: 0.12, Autumn: 0.3, Winter: 0.32 })[seasonOf(d)] || 0.2;""")
rep("""  S.event = chance(0.7) ? pick(EVENTS.filter(e => !e.minLvl || e.minLvl <= L)).id : null;
  S.weather = S.wx36 === 'rain' || S.wx36 === 'dry' ? S.wx36 : (chance(0.2) ? 'rain' : 'dry'); S.wx36 = chance(0.2) ? 'rain' : 'dry';""",
    """  S.weather = S.wx36 === 'rain' || S.wx36 === 'dry' ? S.wx36 : (chance(rain48(S.day)) ? 'rain' : 'dry'); S.wx36 = chance(rain48(S.day + 1)) ? 'rain' : 'dry';
  S.event = chance(0.7) ? pick(EVENTS.filter(e => (!e.minLvl || e.minLvl <= L) && evFits48(e))).id : null;""")
rep("const wx36 = () => (S.wx36 === 'rain' || S.wx36 === 'dry' ? S.wx36 : (S.wx36 = chance(0.2) ? 'rain' : 'dry'));",
    "const wx36 = () => (S.wx36 === 'rain' || S.wx36 === 'dry' ? S.wx36 : (S.wx36 = chance(rain48(S.day + 1)) ? 'rain' : 'dry'));")
# tests: what today's event and weather are, and every event's fit for a given day and weather
rep("const evNow = () => (S && S.event ? EVENTS.find(e => e.id === S.event) : null) || null;",
    "const evNow = () => (S && S.event ? EVENTS.find(e => e.id === S.event) : null) || null;\nwindow.__ev48 = (day, wx) => { const d0 = S.day, w0 = S.weather; if (day) S.day = day; if (wx) S.weather = wx; const out = { season: seasonOf(S.day), fits: EVENTS.filter(e => evFits48(e)).map(e => e.id), rain: rain48(S.day), now: S.event, weather: w0 }; S.day = d0; S.weather = w0; return out; };")
f.save()
print('p48a ok')
