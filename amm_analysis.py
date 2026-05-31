import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.rcParams['font.family'] = 'DejaVu Sans'
output_dir = "E:\\PYTHON_PRACTICE_PORTFOLIO\\dao_research"

# ============================================================
# 第一部分：无常损失计算
# ============================================================

def impermanent_loss(price_ratio):
    """
    计算无常损失
    price_ratio: 当前价格 / 入场价格
    返回：无常损失百分比（负数表示损失）
    """
    il = 2 * np.sqrt(price_ratio) / (1 + price_ratio) - 1
    return il * 100

# 价格变化范围：从原价的0.1倍到10倍
price_ratios = np.linspace(0.1, 10, 1000)
il_values = [impermanent_loss(r) for r in price_ratios]

# ============================================================
# 第二部分：滑点计算
# ============================================================

def calculate_slippage(pool_eth, pool_usdc, trade_eth):
    """
    计算用trade_eth个ETH换USDC时的滑点
    返回：实际均价，理论价格，滑点百分比
    """
    k = pool_eth * pool_usdc
    theoretical_price = pool_usdc / pool_eth
    new_pool_eth = pool_eth + trade_eth
    new_pool_usdc = k / new_pool_eth
    usdc_received = pool_usdc - new_pool_usdc
    actual_price = usdc_received / trade_eth
    slippage = (theoretical_price - actual_price) / theoretical_price * 100
    return actual_price, theoretical_price, slippage

# 池子初始状态：1000 ETH，2,000,000 USDC
pool_eth = 1000
pool_usdc = 2_000_000

# 不同交易规模的滑点
trade_sizes = np.linspace(1, 500, 100)
slippages = []
for size in trade_sizes:
    _, _, slip = calculate_slippage(pool_eth, pool_usdc, size)
    slippages.append(slip)

# ============================================================
# 第三部分：可视化
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("AMM Mechanics: Impermanent Loss & Slippage", fontsize=14)

# 图1：无常损失
axes[0].plot(price_ratios, il_values, color="#E74C3C", linewidth=2)
axes[0].axhline(y=0, color="black", linestyle="--", alpha=0.3)
axes[0].axvline(x=1, color="gray", linestyle="--", alpha=0.5, label="Entry price")
axes[0].fill_between(price_ratios, il_values, 0, alpha=0.2, color="#E74C3C")
axes[0].set_xlabel("Price Ratio (Current / Entry)")
axes[0].set_ylabel("Impermanent Loss (%)")
axes[0].set_title("Impermanent Loss vs Price Change")
axes[0].set_ylim(-30, 2)

# 标注关键点
for ratio, label in [(2, "2x"), (4, "4x"), (0.5, "0.5x")]:
    il = impermanent_loss(ratio)
    axes[0].annotate(f"{label}: {il:.1f}%",
                    xy=(ratio, il),
                    xytext=(ratio + 0.3, il - 2),
                    fontsize=9,
                    arrowprops=dict(arrowstyle="->", color="gray"))
axes[0].legend()

# 图2：滑点
axes[1].plot(trade_sizes, slippages, color="#3498DB", linewidth=2)
axes[1].axhline(y=1, color="orange", linestyle="--", alpha=0.7, label="1% threshold")
axes[1].fill_between(trade_sizes, slippages, alpha=0.2, color="#3498DB")
axes[1].set_xlabel("Trade Size (ETH)")
axes[1].set_ylabel("Slippage (%)")
axes[1].set_title(f"Slippage vs Trade Size\n(Pool: {pool_eth} ETH / {pool_usdc:,} USDC)")
axes[1].legend()

# 标注745 ETH那笔大额交易
_, _, slip_745 = calculate_slippage(pool_eth, pool_usdc, 745)
axes[1].annotate(f"745 ETH: {slip_745:.1f}% slippage",
                xy=(745, slip_745),
                xytext=(400, slip_745 - 10),
                fontsize=9,
                arrowprops=dict(arrowstyle="->", color="gray"))

plt.tight_layout()

img_path = os.path.join(output_dir, "amm_analysis.png")
plt.savefig(img_path, dpi=150, bbox_inches="tight")
print(f"图表已保存到：{img_path}")

# 打印关键数据
print("\n=== 无常损失关键数据点 ===")
for ratio in [1.25, 1.5, 2, 4, 0.75, 0.5]:
    il = impermanent_loss(ratio)
    print(f"价格变化为原来的{ratio}倍：无常损失 {il:.2f}%")

print("\n=== 滑点关键数据点 ===")
for size in [1, 10, 50, 100, 300, 745]:
    _, theo, slip = calculate_slippage(pool_eth, pool_usdc, size)
    print(f"交易{size} ETH：滑点 {slip:.2f}%，实际价格 {theo*(1-slip/100):.0f} USDC/ETH")

plt.show()