import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        boolean playing = true;

        System.out.println("=================================");
        System.out.println("   WELCOME TO JAVA BLACKJACK!    ");
        System.out.println("=================================");

        while (playing) {
            Deck deck = new Deck();
            deck.shuffle();

            Hand playerHand = new Hand();
            Hand dealerHand = new Hand();

            playerHand.addCard(deck.dealCard());
            dealerHand.addCard(deck.dealCard());
            playerHand.addCard(deck.dealCard());
            dealerHand.addCard(deck.dealCard());

            System.out.println("\n--- NEW ROUND ---");
            System.out.println("Dealer shows: " + dealerHand.getCards().get(0) + " | [Hidden Card]");
            System.out.println("Your hand:    " + playerHand + "(Total: " + playerHand.getValue() + ")");

            boolean playerBusted = false;
            while (true) {
                if (playerHand.getValue() == 21) {
                    System.out.println("\n🌟 BLACKJACK! You hit 21! 🌟");
                    break;
                }
                System.out.print("\nDo you want to (H)it or (S)tand? ");
                String choice = scanner.nextLine().trim().toUpperCase();

                if (choice.equals("H")) {
                    Card newCard = deck.dealCard();
                    playerHand.addCard(newCard);
                    System.out.println("You drew: " + newCard);
                    System.out.println("Your hand: " + playerHand + "(Total: " + playerHand.getValue() + ")");

                    if (playerHand.getValue() > 21) {
                        System.out.println("\n💥 BUST! You went over 21!");
                        playerBusted = true;
                        break;
                    }
                } else if (choice.equals("S")) {
                    System.out.println("You stand with a total of " + playerHand.getValue() + ".");
                    break;
                } else {
                    System.out.println("Invalid input. Please type H to Hit or S to Stand.");
                }
            }

            if (!playerBusted) {
                System.out.println("\n--- DEALER'S TURN ---");
                System.out.println("Dealer reveals full hand: " + dealerHand + "(Total: " + dealerHand.getValue() + ")");

                while (dealerHand.getValue() < 17) {
                    System.out.println("Dealer hits...");
                    Card newCard = deck.dealCard();
                    dealerHand.addCard(newCard);
                    System.out.println("Dealer drew: " + newCard);
                    System.out.println("Dealer's hand: " + dealerHand + "(Total: " + dealerHand.getValue() + ")");
                }

                int playerTotal = playerHand.getValue();
                int dealerTotal = dealerHand.getValue();

                System.out.println("\n--- FINAL RESULTS ---");
                if (dealerTotal > 21) {
                    System.out.println("🎉 Dealer busts with " + dealerTotal + "! YOU WIN! 🎉");
                } else if (playerTotal > dealerTotal) {
                    System.out.println("🎉 You win! (" + playerTotal + " vs Dealer's " + dealerTotal + ") 🎉");
                } else if (dealerTotal > playerTotal) {
                    System.out.println("😔 Dealer wins. (" + dealerTotal + " vs Your " + playerTotal + ") 😔");
                } else {
                    System.out.println("🤝 It's a Push! (Tie at " + playerTotal + ") 🤝");
                }
            } else {
                System.out.println("\n--- FINAL RESULTS ---");
                System.out.println("😔 Dealer wins because you busted. 😔");
            }

            System.out.print("\nDo you want to play another round? (Y/N): ");
            String playAgain = scanner.nextLine().trim().toUpperCase();
            if (!playAgain.equals("Y")) {
                playing = false;
                System.out.println("\nThanks for playing Java Blackjack! Goodbye!");
            }
        }
        scanner.close();
    }
}