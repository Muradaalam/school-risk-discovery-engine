
package com.schoolrde.schoolservice.dao.bussiness;

import java.util.List;
import java.util.Optional;

import com.schoolrde.schoolservice.entity.SchoolEntity;
import com.schoolrde.schoolservice.entity.SchoolEntireEntity;

public interface SchoolDao {

    SchoolEntity save(SchoolEntity school);

    Optional<SchoolEntity> findBySchoolId(String schoolId);

    Optional<SchoolEntireEntity> findById(Integer id);

    boolean existsBySchoolId(String schoolId);

    List<SchoolEntireEntity> findTop50SchoolsByPriorityScore();

    List<SchoolEntireEntity> searchSchools(
        String query,
        Integer priorityScore
    );

    void deleteBySchoolId(String schoolId);
}
