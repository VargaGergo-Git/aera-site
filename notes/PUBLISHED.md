# Published field notes ledger

Track what shipped, the chatbot question it answers, and the corpus source. INDEX.md in the private Aera repo is extraction order only; pick the next unpublished article by chatbot-ask likelihood, not by INDEX line order.

| Date | Slug | Question (title/meta) | Editorial h1 | Corpus id | Why this order |
| --- | --- | --- | --- | --- | --- |
| 2026-09-22 | what-does-walking-pace-say-about-fitness | What does walking pace say about fitness? | Your walking pace | body.walkingPace | Next in PUBLISH-ORDER; everyday gait/fitness ask after movement live |
| 2026-09-22 | what-is-cardio-load | What is cardio load? | Cardio load | fitness.cardioLoad | Next in PUBLISH-ORDER; load-vs-base ask after strain/zones live |
| 2026-09-22 | what-is-workout-effort | What is workout effort? | Workout effort | fitness.workoutEffort | Completes effort/load pair; perceived exertion ask after cardio load |
| 2026-09-21 | what-does-blood-oxygen-on-a-watch-mean | What does blood oxygen on a watch mean? | Blood oxygen on a watch | body.spo2 | Next in PUBLISH-ORDER; overnight SpO2 ask after breathing/sleeping HR live |
| 2026-09-21 | what-does-wrist-skin-temperature-mean | What does wrist skin temperature mean? | Wrist skin temperature | body.skinTemp | Next in PUBLISH-ORDER; overnight relative-temp ask after breathing cluster |
| 2026-09-21 | how-much-daily-movement-matters | How much daily movement matters? | Why daily movement adds up | longevity.movement | Completes everyday steps ask; pairs with Zone 2 / VO2 / all-day HR |
| 2026-09-20 | what-is-zone-2-training | What is Zone 2 training? | Building your aerobic base | heart.zone2 | Next in PUBLISH-ORDER; everyday easy-effort ask after all-day HR |
| 2026-09-20 | what-are-heart-rate-zones | What are heart rate zones? | Heart rate zones | fitness.hrZones | Next in PUBLISH-ORDER; pairs with Zone 2; shape-vs-average ask |
| 2026-09-20 | what-is-overnight-breathing-rate | What is overnight breathing rate? | Your breathing rate at night | body.respiratoryRate | Completes overnight cluster with sleeping HR/RHR/HRV; early-drift ask |
| 2026-09-19 | what-moved-my-recovery | What moved my recovery? | What moved with your recovery | recovery.why | Next in PUBLISH-ORDER; everyday co-occurrence ask after recovery/cost/balance live |
| 2026-09-19 | why-does-the-week-matter-for-stress | Why does the week matter for stress? | Why the week matters | recovery.cumulativeStress | Next in PUBLISH-ORDER; week-context ask after stress/balance live |
| 2026-09-19 | what-does-all-day-heart-rate-tell-me | What does all-day heart rate tell me? | Your heart rate, all day | heart.allDay | Completes heart cluster with RHR/HRV/sleeping HR; everyday all-day chart ask |
| 2026-09-18 | what-is-sleep-architecture | What is sleep architecture? | More than its hours | sleep.architecture | Next in PUBLISH-ORDER; everyday shape-of-the-night ask after duration cluster |
| 2026-09-18 | what-does-a-hard-day-cost-me | What does a hard day cost me? | What a hard day usually costs you | recovery.cost | Next in PUBLISH-ORDER; everyday post-hard-day ask after recovery/strain live |
| 2026-09-18 | how-do-i-balance-push-and-rest | How do I balance push and rest? | Balancing push and rest | recovery.balance | Completes cost/strain/recovery cluster; push-rest ask after cost |
| 2026-09-17 | how-fast-should-my-heart-settle-after-exercise | How fast should my heart settle after exercise? | How fast your heart settles | heart.hrRecovery | Next in PUBLISH-ORDER; everyday post-workout ask after RHR/HRV/strain live |
| 2026-09-17 | what-is-vo2max-on-a-watch | What is VO2max on a watch? | VO2max on a watch | longevity.vo2 | Everyday fitness ceiling ask; pairs with strain and readiness |
| 2026-09-17 | how-much-time-asleep-vs-time-in-bed | How much time asleep vs time in bed? | Time asleep versus time in bed | longevity.timeAsleep | Completes duration cluster with sleep need, debt, and stages |
| 2026-09-15 | what-is-a-bedtime-window | What is a bedtime window? | Your bedtime window | sleep.bedtimeWindow | Next in PUBLISH-ORDER; everyday timing ask after body clock |
| 2026-09-15 | what-does-stress-mean-on-a-watch | What does stress mean on a watch? | Stress as a signal | recovery.stress | Everyday watch word; pairs with recovery and HRV already live |
| 2026-09-15 | what-is-training-strain | What is training strain? | Training strain and load | recovery.strain | Completes stress/recovery/strain trio; readiness sibling live |
| 2026-09-14 | what-does-recovery-actually-measure | What does recovery actually measure? | What recovery actually measures | recovery.basics | Next in PUBLISH-ORDER; everyday morning-number ask after sleep cluster |
| 2026-09-14 | what-is-sleeping-heart-rate | What is sleeping heart rate? | Your sleeping heart rate | heart.sleepingHR | Pairs with RHR/HRV; clarifies overnight vs awake resting labels |
| 2026-09-14 | what-is-my-body-clock | What is my body clock / circadian rhythm? | Your body clock | sleep.bodyClock | Completes timing trio with regularity and sleep need |
| 2026-09-12 | what-is-sleep-debt | What is sleep debt? | Sleep debt and the reserve | sleep.debt | Next in PUBLISH-ORDER; everyday chatbot ask after overnight heart trio |
| 2026-09-12 | does-sleep-regularity-matter-more-than-duration | Does sleep regularity matter more than duration? | Why sleep timing may matter more than hours | longevity.sleepRegularity | Pairs with sleep need and debt; Windred 2024 already in corpus |
| 2026-09-12 | what-does-a-sleep-score-mean | What does a sleep score mean? | What a sleep score actually means | sleep.score | Completes sleep morning-number cluster with stages + debt |
| 2026-09-11 | what-is-hrv | What is HRV? | What heart rate variability actually is | longevity.hrv | Next in PUBLISH-ORDER after sleep.need/stages; constant chatbot ask; overnight autonomic pair with RHR |
| 2026-09-11 | what-does-a-readiness-score-mean | What does a readiness score mean? | What a readiness score actually means | fitness.trainingReadiness | Everyday training-app question; load + false-green evidence already in corpus |
| 2026-09-11 | why-is-my-resting-heart-rate-up | Why is my resting heart rate up? | Why resting heart rate rises | longevity.rhr | Completes the overnight heart pair with HRV; high everyday ask |
| 2026-09-10 | how-much-sleep-you-actually-need | How much sleep do I actually need? | How much sleep you actually need | sleep.need | Highest everyday chatbot ask after sleep-stage accuracy; NSF range + regularity evidence already in corpus |
| 2026-09-09 | watch-sleep-stages-are-an-estimate | Are Apple Watch sleep stages accurate? | Your watch's sleep stages are an estimate | sleep.stages | Highest chatbot ask for watch owners; validation literature already in corpus |

Remaining of 62: 30 unpublished / thirty-two live.
