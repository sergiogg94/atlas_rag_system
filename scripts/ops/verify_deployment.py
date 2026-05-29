import httpx
import asyncio

SERVICES = {
    "backend": "https://atlas-backend-qgq0.onrender.com/health",
    "frontend": "https://atlas-frontend-2cca.onrender.com",
    "dashboard": "https://atlas-dashboard-pvib.onrender.com",
}


async def check_service(name: str, url: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name} is running.")
                return True
            else:
                print(f"❌ {name} is unhealthy. Status code: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Error checking {name}: {str(e)}")
        return False


async def verify_all():
    print("Verifying deployment...")

    results = {}
    for name, url in SERVICES.items():
        results[name] = await check_service(name, url)


if __name__ == "__main__":
    asyncio.run(verify_all())
