import httpx
import asyncio
import time

SERVICES = {
    "backend": "https://atlas-backend-qgq0.onrender.com/health",
    "frontend": "https://atlas-frontend-2cca.onrender.com",
    "dashboard": "https://atlas-dashboard-pvib.onrender.com",
}


async def warmup_service(name: str, url: str):
    print(f"🔄 Warmup {name}...")
    start = time.time()

    try:
        async with httpx.AsyncClient(timeout=65.0) as client:
            response = await client.get(url)
            elapsed = time.time() - start

            if response.status_code == 200:
                print(f"✅ {name} responds in {elapsed:.1f}s")
                return True
            else:
                print(f"⚠️  {name} returns status {response.status_code}")
                return False
    except Exception as e:
        elapsed = time.time() - start
        print(f"❌ {name} failed after {elapsed:.1f}s: {str(e)}")
        return False


async def warmup_all():
    """Warmp up all services by sending a request to each one."""
    print("🚀 Warmup all services from Atlas RAG System")
    print("=" * 60)
    print("⏱️ This can take a while...")
    print()

    tasks = [warmup_service(name, url) for name, url in SERVICES.items()]
    results = await asyncio.gather(*tasks)

    print("\n" + "=" * 60)
    if all(results):
        print("✅ All services are ready!")
    else:
        print("⚠️  Some services may not be fully ready.")


if __name__ == "__main__":
    asyncio.run(warmup_all())
