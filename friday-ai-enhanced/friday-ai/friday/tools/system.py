"""
friday/tools/system.py – System information tools
"""
import datetime
import platform
import psutil
import pytz


def get_current_time(timezone: str = "Asia/Colombo") -> str:
    """Get the current date and time, optionally in a specific timezone."""
    try:
        tz  = pytz.timezone(timezone)
        now = datetime.datetime.now(tz)
        return now.strftime(f"%A, %B %d %Y — %I:%M %p (%Z)")
    except Exception:
        now = datetime.datetime.now()
        return now.strftime("%A, %B %d %Y — %I:%M %p")


def get_system_info() -> str:
    """Get full system hardware and OS information — Stark Industries diagnostic report."""
    cpu_pct  = psutil.cpu_percent(interval=1)
    mem      = psutil.virtual_memory()
    disk     = psutil.disk_usage("/")
    boot_ts  = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime   = datetime.datetime.now() - boot_ts
    hours, r = divmod(int(uptime.total_seconds()), 3600)
    minutes  = r // 60

    return (
        f"OS: {platform.system()} {platform.release()} ({platform.machine()})\n"
        f"CPU Usage: {cpu_pct}%  |  Cores: {psutil.cpu_count()}\n"
        f"RAM: {mem.used / 1e9:.1f} GB used / {mem.total / 1e9:.1f} GB total ({mem.percent}%)\n"
        f"Disk: {disk.used / 1e9:.1f} GB used / {disk.total / 1e9:.1f} GB total ({disk.percent}%)\n"
        f"System uptime: {hours}h {minutes}m"
    )


def get_battery_status() -> str:
    """Check battery status of the system."""
    battery = psutil.sensors_battery()
    if battery is None:
        return "No battery detected — running on AC power (desktop system)."
    plugged = "Plugged in" if battery.power_plugged else "On battery"
    return (f"Battery: {battery.percent:.0f}% — {plugged}. "
            f"{'Charging' if battery.power_plugged else f'~{int(battery.secsleft/60)} min remaining'}")


def get_running_processes(top_n: int = 5) -> str:
    """List the top N CPU-consuming processes."""
    procs = sorted(psutil.process_iter(["pid", "name", "cpu_percent"]),
                   key=lambda p: p.info["cpu_percent"] or 0, reverse=True)[:top_n]
    lines = [f"{p.info['name']} (PID {p.info['pid']}) — {p.info['cpu_percent']}% CPU"
             for p in procs]
    return "Top processes:\n" + "\n".join(lines)
