# HRMS Troubleshooting Guide

## Common Setup Issues and Solutions

### 1. TypeScript Version Conflict (SOLVED)

**Error:**
```
npm error ERESOLVE could not resolve
npm error While resolving: react-scripts@5.0.1
npm error Found: typescript@5.9.2
npm error Could not resolve dependency:
npm error peerOptional typescript@"^3.2.1 || ^4" from react-scripts@5.0.1
```

**Solution:**
- Updated `package.json` to use TypeScript `^4.9.5` (compatible with react-scripts@5.0.1)
- Added `--legacy-peer-deps` flag to npm install in Dockerfile
- Simplified dependency versions for better compatibility

### 2. Docker Permission Issues

**Error:**
```
permission denied while trying to connect to the Docker daemon socket
```

**Solutions:**

**Option A: Add user to docker group (Recommended)**
```bash
sudo usermod -aG docker $USER
newgrp docker
# Then logout and login again, or restart your session
```

**Option B: Run with sudo**
```bash
sudo docker-compose up --build
```

**Option C: Check Docker service**
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### 3. Port Conflicts

**Error:**
```
Port 3000/5000/5432 is already in use
```

**Solution:**
```bash
# Check what's using the ports
sudo netstat -tulpn | grep :3000
sudo netstat -tulpn | grep :5000
sudo netstat -tulpn | grep :5432

# Kill processes using the ports
sudo kill -9 <PID>

# Or modify docker-compose.yml to use different ports
```

### 4. Frontend Build Issues

**If you encounter React/TypeScript errors:**

1. **Clear npm cache:**
   ```bash
   docker exec -it hrms_frontend npm cache clean --force
   ```

2. **Reinstall dependencies:**
   ```bash
   docker exec -it hrms_frontend rm -rf node_modules package-lock.json
   docker exec -it hrms_frontend npm install --legacy-peer-deps
   ```

3. **Rebuild frontend container:**
   ```bash
   docker-compose down
   docker-compose up --build frontend
   ```

### 5. Backend Python Issues

**If you encounter Python import errors:**

1. **Check Python dependencies:**
   ```bash
   docker exec -it hrms_backend pip list
   ```

2. **Reinstall requirements:**
   ```bash
   docker exec -it hrms_backend pip install -r requirements.txt
   ```

3. **Check Python path:**
   ```bash
   docker exec -it hrms_backend python -c "import sys; print(sys.path)"
   ```

### 6. Database Connection Issues

**Error:**
```
could not connect to server: Connection refused
```

**Solutions:**

1. **Check if PostgreSQL container is running:**
   ```bash
   docker-compose ps
   ```

2. **Check PostgreSQL logs:**
   ```bash
   docker-compose logs postgres
   ```

3. **Recreate database volume:**
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```

### 7. Container Won't Start

**Check container logs:**
```bash
docker-compose logs [service_name]
```

**Common issues:**
- Missing environment variables
- Port conflicts
- File permission issues
- Dependency conflicts

### 8. API Endpoints Not Working

1. **Check backend is running:**
   ```bash
   curl http://localhost:5000/health
   ```

2. **Check API documentation:**
   - Visit: http://localhost:5000/docs

3. **Check CORS settings:**
   - Ensure frontend URL is in CORS allowed origins

### 9. Database Schema Issues

**Reset database:**
```bash
docker-compose down -v
docker-compose up --build
```

**Manual database access:**
```bash
docker exec -it hrms_postgres psql -U hrms_user -d hrms_db
```

### 10. Performance Issues

**Increase Docker resources:**
- Memory: At least 4GB
- CPU: At least 2 cores

**Check system resources:**
```bash
docker stats
```

## Quick Fixes Checklist

- [ ] Docker is running: `docker --version`
- [ ] Docker Compose is installed: `docker-compose --version`
- [ ] User has Docker permissions: `docker ps`
- [ ] Ports 3000, 5000, 5432 are free
- [ ] System has enough resources (4GB+ RAM)
- [ ] All environment files are present
- [ ] No conflicting containers running

## Development Commands

**Start fresh:**
```bash
docker-compose down -v
docker-compose up --build
```

**View all logs:**
```bash
docker-compose logs -f
```

**Enter containers:**
```bash
docker exec -it hrms_frontend bash
docker exec -it hrms_backend bash
docker exec -it hrms_postgres psql -U hrms_user -d hrms_db
```

**Check container status:**
```bash
docker-compose ps
docker stats
```

## Getting Help

1. Check this troubleshooting guide
2. Review `DEVELOPMENT_GUIDE.md`
3. Check container logs: `docker-compose logs [service]`
4. Verify environment configuration
5. Try the setup script: `./setup.sh`

## Useful Commands Summary

```bash
# Setup and start
./setup.sh

# Manual start
docker-compose up --build

# Stop everything
docker-compose down

# Complete reset
docker-compose down -v
docker system prune -f
docker-compose up --build

# View logs
docker-compose logs -f [service_name]

# Check status
docker-compose ps
```
