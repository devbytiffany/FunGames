package game2_blackjack_java;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Deck {
    private List<Card> cards;
    public Deck(){
        cards = new ArrayList<>();
        String[] suits ={ "Hearts","Diaamonds", "Clubs", "Spades"};
        String[] ranks = {"2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"};

        for (String suit: suits){
            for (int i =0; i < ranks.length; i++){
                String rank = ranks [i];
                int value;

                if (rank.equals("Jack") || rank.equals("Queen")|| rank.equals("King")){
                    value = 10;
                } else if (rank.equals("Ace")){
                    value = 11;
                } else{
                    value =Integer.parseInt(rank);
                }

                cards.add(new Card (suit, rank, value));
            }
        }
    } 

    public void shuffle(){
        Collections.shuffle(cards);
    }

    public Card dealCard(){
        if (cards.isEmpty()){
            return null;
        }
        return cards.remove(0);
    }
    public int remainingCards(){
        return cards.size();
    }
}
