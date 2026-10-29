package com.schoolrde.schoolservice.dao.bussiness;



import java.util.Optional;
import org.springframework.stereotype.Repository;

import com.schoolrde.schoolservice.dao.repository.EventRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.schoolrde.schoolservice.entity.EventEntity;

@Repository
public class EventDaoImpl implements EventDao{

	private static final Logger LOGGER = LoggerFactory.getLogger(EventDaoImpl.class);

	private final EventRepository eventRepository;

	public EventDaoImpl(EventRepository eventRepository){
        this.eventRepository=eventRepository;
    }
    
	@Override
    public Optional<EventEntity> findById(Integer id){
    	LOGGER.info("Quering event from database with id : {}", id);
        return eventRepository.findById(id);
    }

}