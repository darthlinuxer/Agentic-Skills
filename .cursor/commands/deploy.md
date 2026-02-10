Before answering:
- Apply the most relevant skills and rules for this platform.
- Prefer the single most specific skill/rule when possible.
- If no skill or rule clearly matches, ignore all and answer normally.

# /deploy - Production Deployment

$ARGUMENTS

## Purpose
Handle production deployment with pre-flight checks, deployment execution, and verification.

## Sub-commands
```
/deploy            - Interactive deployment wizard
/deploy check      - Run pre-deployment checks only
/deploy preview    - Deploy to preview/staging
/deploy production - Deploy to production
/deploy rollback   - Rollback to previous version
```

## Pre-Deployment Checklist
```markdown
## 🚀 Pre-Deploy Checklist

### Code Quality
- [ ] No TypeScript errors (`npx tsc --noEmit`)
- [ ] ESLint passing (`npx eslint .`)
- [ ] All tests passing (`npm test`)

### Security
- [ ] No hardcoded secrets
- [ ] Environment variables documented
- [ ] Dependencies audited (`npm audit`)

### Performance
- [ ] Bundle size acceptable
- [ ] No console.log statements
- [ ] Images optimized

### Documentation
- [ ] README updated
- [ ] CHANGELOG updated
- [ ] API docs current
```

## Output Format
### Successful Deploy
```markdown
## 🚀 Deployment Complete

### Summary
- **Version:** v1.2.3
- **Environment:** production
- **Duration:** 47 seconds
- **Platform:** Vercel

### URLs
- 🌐 Production: 
- 📊 Dashboard: 

### What Changed
- Added user profile feature
- Fixed login bug
- Updated dependencies

### Health Check
✅ API responding (200 OK)
✅ Database connected
✅ All services healthy
```

### Failed Deploy
```markdown
## ❌ Deployment Failed

### Error
Build failed at step: TypeScript compilation

### Details
```
error TS2345: Argument of type 'string' is not assignable...
```

### Resolution
1. Fix TypeScript error in `src/services/user.ts:45`
2. Run `npm run build` locally to verify
3. Try `/deploy` again
```

## Platform Support
| Platform | Command | Notes |
|----------|---------|-------|
| Vercel | `vercel --prod` | Auto-detected for Next.js |
| Railway | `railway up` | Needs Railway CLI |
| Fly.io | `fly deploy` | Needs flyctl |
| Docker | `docker compose up -d` | For self-hosted |

## Examples
```
/deploy
/deploy check
/deploy preview
/deploy production --skip-tests
/deploy rollback
```
