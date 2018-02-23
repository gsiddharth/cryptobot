import crypto_data
import argparse

def arbitrage(ex1, ex2, sym1_ex1, sym2_ex1, sym_ex2):
    bid_ex1_sym1 = crypto_data.get(ex1, sym1_ex1, "bid")
    bid_ex1_sym2 = crypto_data.get(ex1, sym2_ex1, "bid")
    bid_ex2_sym = crypto_data.get(ex2, sym_ex2, "bid")
    
    ask_ex1_sym1 = crypto_data.get(ex1, sym1_ex1, "ask")
    ask_ex1_sym2 = crypto_data.get(ex1, sym2_ex1, "ask")
    ask_ex2_sym = crypto_data.get(ex2, sym_ex2, "ask")

    arb_buy = round(((bid_ex1_sym1/ask_ex1_sym2 - ask_ex2_sym)/ask_ex2_sym) * 100.0, 2)
    arb_sell = round(((bid_ex2_sym - ask_ex1_sym1/bid_ex1_sym2 )/bid_ex2_sym) * 100.0, 2)

    return (arb_buy, arb_sell)

def main():
    arg_parser = argparse.ArgumentParser(description = "Crypto currency prices")    
    arg_parser.add_argument("ex1", help = "Exchange 1")
    arg_parser.add_argument("ex2", help = "Exchange 2")
    arg_parser.add_argument("sym1_ex1", help = "Symbol 1 on Exchange 1")
    arg_parser.add_argument("sym2_ex1", help = "Symbol 2 on Exchange 1")
    arg_parser.add_argument("sym_ex2", help = "Symbol on Exchange 2")    

    args = arg_parser.parse_args()

    print(arbitrage(args.ex1, args.ex2, args.sym1_ex1, args.sym2_ex1, args.sym_ex2))

if __name__ == "__main__":
    main()




